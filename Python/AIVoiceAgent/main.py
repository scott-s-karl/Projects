import asyncio
import base64 # Encoding used for sending audio
import json
import websockets # module that we installed at the beginning
import os 

from dotenv import load_dotenv 

# ===================
# Terminology Notes:
# ===================
# sts is our voice agent while twilio is for twilio 

# This is going to load the environment variable from out local .env file
load_dotenv()


def sts_connect():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise Exception("DEEPGRAM_API_KEY not found")
    
    # As soon as we spin up the server we:
    # 1. Connect to Deepgram
    # 2. Provide the API token
    # 3. Listen for anytime that we receive a phonecall
    # 4. We can then respond
    # Order:
    # 1. We call the phone number 
    # 2. Phone number hosted by twilio
    # 3. Twilio routes the request to our server
    # 4. Our server connects to Deepgram and we can communicate back and forth with deepgram to get the new text/voice that we should speak
    # 5. Send that response back to Twilio and Twilio speaks it to us
    sts_ws = websockets.connect(
        "wss://agent.deepgram.com/v1/agent/converse",
        subprotocols = ["token", api_key]
        )
    return sts_ws

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)
    
async def handle_barge_in(decoded, twilio_ws, streamsid):
    # User starts speaking while the AI is still speaking
    if decoded["type"] == "UserStartedSpeaking":
        clear_message = {
            "event":"clear",
            "streamSid": streamsid
        }

        # Send the clear message to Twilio to interupt the model and make it stop speaking
        await twilio_ws.send(json.dumps(clear_message))

async def handle_text_message(decoded, twilio_ws, sts_ws, streamsid):
    await handle_barge_in(decoded, twilio_ws, streamsid)

    # To do: Handle function calling

async def sts_sender(sts_ws, audio_queue):
    print("sts sender started")
    while True:
        chunk = await audio_queue.get() # As soon as we have something in the audio queue
        await sts_ws.send(chunk) # Send it to Deepgram

async def sts_receiver(sts_ws, twilio_ws, streamsid_queue):
    print("sts receiver started")
    
    streamsid = await streamsid_queue.get() # Waits until we received a stream SID from twilio

    # For each message received back from Deepgram
    async for message in sts_ws:
        # If its text then its an event that we should respond to - calling a function, etc...
        if type(message) is str:
            print(message)
            decoded = json.loads(message)
            await handle_text_message(decoded, twilio_ws, sts_ws, streamsid)
            continue

        # Raw message which is bytes coming from Deepgram - The voice we want to send to Twilio so it can speak it
        raw_mulaw = message

        media_message = {
            "event": "media",
            "streamSid": streamsid,
            "media": {"payload": base64.b64encode(raw_mulaw).decode("ascii")}
        }

        # Take the message convert it to a string and send it to Twilio
        await twilio_ws.send(json.dumps(media_message))


async def twilio_receiver(twilio_ws, audio_queue, streamsid_queue):
    print("twilio_receiver started")

    # Note: 
    # Twilio sends audio data as 160 byte messages containing 20ms of audio each
    # we will buffer 20 twilio messages corresponding to 0.4 seconds of audio to improve 
    # throughput performance
            
    BUFFER_SIZE = 20 * 160
    inbuffer = bytearray(b"")

    # Connect and loop through all of the message chunks that are being received
    async for message in twilio_ws:
        # Load in the data
        try:
            data = json.loads(message)
            event = data["event"] # Start, Connected, Media

            # check the event
            if event == "start":
                print("Get our streams id")
                start = data["start"]
                streamsid = start["streamSid"]
                streamsid_queue.put_nowait(streamsid)

            elif event == "connected":
                continue

            elif event == "media": # Audio 
                media = data["media"]
                chunk = base64.b64decode(media["payload"]) # Taking the bytes "payload of the users voice and decoding it

                if media["track"] == "inbound":
                    inbuffer.extend(chunk)

            elif event == "stop":
                break

            # Only send data to Deepgram once it fills the buffer limit we set
            while len(inbuffer) >= BUFFER_SIZE:
                chunk = inbuffer[:BUFFER_SIZE]  # Get the chunk in our inbuffer equal to out limit
                audio_queue.put_nowait(chunk) # Add it to the audio queue for Deepgram
                inbuffer = inbuffer[BUFFER_SIZE:] # Remove chunk from the buffer
        except:
            break

async def twilio_handler(twilio_ws):
    audio_queue = asyncio.Queue() # Stores all of the audio that we need to respond to
    streamsid_queue = asyncio.Queue() # Represent the current active streams from twilio - ids of the active connections to twilio

    # Allow us to connect to Deepgram - this runs when someone connects 
    async with sts_connect() as sts_ws:
        # Allows Deepgram to setup based on our config data
        config_message = load_config() # Message
        await sts_ws.send(json.dumps(config_message)) # Send via websocket to Deepgram (json.dumps - Converts to stream)

        # Setup background running tasks
        await asyncio.wait(
            [
                asyncio.ensure_future(sts_sender(sts_ws, audio_queue)), # Always able to send things to Deepgram 
                asyncio.ensure_future(sts_receiver(sts_ws, twilio_ws, streamsid_queue)), # Always able to receive things from Deepgram
                asyncio.ensure_future(twilio_receiver(twilio_ws, audio_queue, streamsid_queue)) # Always able to receive things from twilio
            ]
        )

        # Await the end of the twilio websocket
        await twilio_ws.close()

async def main():
    
    # Essentially any time a call comes in the twilio handler function will get called and create new sender, receivers, etc...

    # Makes sure that the server is always running
    await websockets.serve(twilio_handler, host = "localhost", port = 5000)
    print("Started Server")

    # Keep running until we exit out of the code manually
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
