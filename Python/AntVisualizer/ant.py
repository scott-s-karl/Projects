# Imports
# ---------------

import pygame
import math
import time
import pdb 

# Set global initials
pygame.init()
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Four Ants in a Square Visualizer")
font = pygame.font.Font(None, 36)  # Use default font, size 36

# Define colors for use in visualization
RED       = (255, 0, 0)
GREEN     = (0, 255, 0)
BLUE      = (0, 0, 255)
YELLOW    = (255, 255, 0)
WHITE     = (255, 255, 255)
BLACK     = (0, 0, 0)
PURPLE    = (128, 0, 128)
ORANGE    = (255, 165, 0)
GREY      = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Ant:
    def __init__(self, name, color, x, y, image):
        self.name = name
        self.color = color
        self.radius = 5
        self.x = x
        self.y = y
        self.start_position = self.get_pos()
        self.partner = None
        self.move_unit = 5
        self.distance_moved = 0
        self.points_covered = []
        self.image = image

    def store_point(self):
        self.points_covered.append(self.get_pos())
    
    def get_pos(self):
        return (self.x, self.y)
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, width=0)

    def point_along_line(self, p2, d):
        x1, y1 = self.x, self.y
        x2, y2 = p2

        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)  # same as sqrt(dx**2 + dy**2)

        if length == 0:
            raise ValueError("Points P1 and P2 are the same!")

        unit_dx = dx / length
        unit_dy = dy / length

        new_x = x1 + unit_dx * d
        new_y = y1 + unit_dy * d

        return (new_x, new_y)
    
    def move(self, partner_x, partner_y):
        self.store_point()
        x, y = self.point_along_line((partner_x, partner_y), 1)
        self.x = x
        self.y = y
        self.distance_moved +=1


def draw_screen(win, ants, label_surface, paused, run):
    tl = 100 # Top Left
    tr = 100 # Top Right
    wh = 600 # Width/Height

    # Fill main window
    win.fill(GREY)

    # Draw the label
    win.blit(label_surface, (400 - (label_surface.get_width()/2), 30))

    # Draw Square
    pygame.draw.rect(win, BLACK, (tl, tr, wh, wh))
    size_label = font.render(str(wh), True, BLACK)
    win.blit(size_label, (400 - size_label.get_width()/2, 100 - size_label.get_height() - 5))
    win.blit(size_label, (400 - size_label.get_width()/2, 700 + 5))

    rotated_surface_pos90 = pygame.transform.rotate(size_label, 90)
    rotated_surface_neg90 = pygame.transform.rotate(size_label, -90)
    win.blit(rotated_surface_pos90, (100 - size_label.get_height() - 5, 400 - size_label.get_width()/2))
    win.blit(rotated_surface_neg90, (700 + 5, 400 - size_label.get_width()/2))
    
    # Draw the ants
    for ant in ants:
        steps_label = font.render(str(ant.distance_moved), True, ant.color)
        ant.draw(win)
        if len(ant.points_covered) > 2:
            pygame.draw.lines(win, ant.color, False, ant.points_covered, 3)
            win.blit(steps_label, ant.start_position)

    # Update
    pygame.display.update()

def check_for_collision(ants):
    for ant in ants:
        cx, cy = ant.get_pos()
        px, py = ant.partner.get_pos()
        if (math.isclose(cx, px, abs_tol=1.5) and math.isclose(cy, py, abs_tol=1.5)):
            return True
    return False

def move_ants(ants):
    # Loop
    for ant in ants:
        # Get the position of partner
        partner_x, partner_y = ant.partner.get_pos()
        ant.move(partner_x, partner_y)
            
    # Check ants
    return check_for_collision(ants)


def main(win, width):
    wh = 600
    square_left = 100
    square_right = square_left + wh
    square_top = 100
    square_bottom = square_top + wh

    # Define the ants
    scale_size = 100
    dad_image = pygame.image.load("Dad.jpeg")
    dad_scaled_image = pygame.transform.scale(dad_image, (scale_size, scale_size)) 
    steven_image = pygame.image.load("steven.jpeg")
    steven_scaled_image = pygame.transform.scale(steven_image, (scale_size, scale_size)) 
    bryan_image = pygame.image.load("Bryan.jpeg")
    byran_scaled_image = pygame.transform.scale(bryan_image, (scale_size, scale_size)) 
    taylor_image = pygame.image.load("Taylor.jpeg")
    taylor_scaled_image = pygame.transform.scale(taylor_image, (scale_size, scale_size)) 

    ant1 = Ant("Ant 1", RED, square_left, square_top, dad_scaled_image)
    ant2 = Ant("Ant 2", BLUE, square_right, square_top, steven_scaled_image)
    ant3 = Ant("Ant 3", GREEN, square_right, square_bottom, byran_scaled_image)
    ant4 = Ant("Ant 4", YELLOW, square_left, square_bottom, taylor_scaled_image)

    ants = [ant1, ant2, ant3, ant4]

    # Assign Partner
    ant1.partner = ant2
    ant2.partner = ant3
    ant3.partner = ant4
    ant4.partner = ant1

    # Label
    not_started = "Press Spacebar to Start"
    paused_label = "Simulation Paused. Press Spacebar to continue"
    running_label =  "Simulation Running"
    done_label = "Simulation Complete. Press Spacebar to close"


    # Define the state

    run = True
    started = False
    paused = False
    close_window = False

    # -- Start of While -- 
    while(run):
        # Check if the game is started or pause
        if not started:
            # Show not started
            label_surface = font.render(not_started, True, BLACK)
        elif started and paused:
            # Show paused
            label_surface = font.render(paused_label, True, BLACK)
        else:
            # Show running
            label_surface = font.render(running_label, True, BLACK)

            # Move the ants
            if move_ants(ants):
                run = False
                label_surface = font.render(done_label, True, BLACK)

        # Draw the screen
        draw_screen(win, ants, label_surface, paused, run)

        # Loop through events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Handle Keydown event
            if event.type == pygame.KEYDOWN:
                # Handle spacebar
                if event.key == pygame.K_SPACE:
                    # Start if not started
                    if not started:
                        started = True

                    # Pause sim otherwise 
                    else:
                        if paused:
                            paused = False
                        else:
                            paused = True

    while(not close_window):
        # Loop through events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Handle Keydown event
            if event.type == pygame.KEYDOWN:
                # Handle spacebar
                if event.key == pygame.K_SPACE:
                    close_window = True
    # -- End of While --
    pygame.quit()


# Call Main
main(WIN, WIN)
