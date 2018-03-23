import pygame
from math import sin, cos, tan, radians, sqrt, atan2


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

# Set the width and height of the screen [width, height]
size = (800, 800)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Omni_simu")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

SIZE = 20
speed_a = 0 #cm.s-1
speed_b = 0
speed_c = 0
yaw = 0
cx = 300
cy = 300
joy = pygame.joystick.Joystick(0)
joy.init()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here
    axis_yaw   = joy.get_axis(0)
    axis_roll  = joy.get_axis(3)
    axis_pitch = joy.get_axis(4)

    speed_cmd = sqrt(axis_roll * axis_roll + axis_pitch * axis_pitch)
    angle_cmd = atan2(axis_pitch, axis_roll) - radians(90)


    print(axis_yaw, axis_roll, axis_pitch)

    #speed_a = 0.5 * axis_yaw + 0.5 * cos(angle_cmd)
    speed_a = 0.5 * axis_yaw + 0.5 * cos(radians(90) + angle_cmd) * speed_cmd
    #speed_b = 0.5 * axis_yaw + 0.5 * cos(radians(60) + angle_cmd)
    speed_b = 0.5 * axis_yaw + 0.5 * cos(radians(210) + angle_cmd) * speed_cmd
    #speed_c = 0.5 * axis_yaw + 0.5 * cos(radians(-60) + angle_cmd)
    speed_c = 0.5 * axis_yaw + 0.5 * cos(radians(-30) + angle_cmd) * speed_cmd
    print('**', speed_a, speed_b, speed_c, yaw)

    #print(axis_yaw)
    vec_a = (speed_a * cos(radians(yaw)), speed_a * -sin(radians(yaw)))
    vec_b = (speed_b * cos(radians(yaw + 120)), speed_b * -sin(radians(yaw + 120)))
    vec_c = (speed_c * cos(radians(yaw - 120)), speed_c * -sin(radians(yaw - 120)))
    vec_res = tuple(map(sum, zip(vec_a, vec_b, vec_c)))
    cx += vec_res[0] * 10
    cy += vec_res[1] * 10
    yaw -= (speed_a + speed_b + speed_c) * 10
    polygon_points = [[cx + SIZE * cos(radians(90 + yaw)),
                       cy - SIZE * sin(radians(90 + yaw))],
                      [cx + SIZE * cos(radians(-30 + yaw)),
                       cy - SIZE * sin(radians(-30 + yaw))],
                      [cx + SIZE * cos(radians(-150 + yaw)),
                       cy - SIZE * sin(radians(-150 + yaw))]]

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)

    # --- Drawing code should go here
    pygame.draw.polygon(screen, BLACK, polygon_points)
    pygame.draw.circle(screen, RED, [int(polygon_points[0][0]), int(polygon_points[0][1])], 5)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(30)

# Close the window and quit.
pygame.quit()
