import numpy as np
import pygame

# initialize Pygame
pygame.init()

# set screen dimensions
screen_width = 800
screen_height = 600
grass_file = pygame.image.load('grass.jpg')
ball_file = pygame.image.load('ball.png')
sand_file = pygame.image.load('sand.jpg')
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Mini Golf Game")

#define score
strokes = 0
# define ball properties
ball_radius = 20
ball_color = (255, 255, 255)
ball_mass = 0.04593
ball_friction_coefficient = 0.02

# define surface properties
grass_friction_coefficient = 0.0026

# define an array of obstacles, their location and radius
obstacles = [
    {"position": np.array([400,200]), "radius": 50},
    {"position": np.array([500,400]), "radius": 75},
    {"position": np.array([300,500]), "radius": 25},
    {"position": np.array([100,300]), "radius": 30},
]

# define sand and its properties
sand_colour = (135, 116, 69)
sandpits = [
    {"position": np.array([400,450]), "size": np.array([200,100])}
]
#sets the current hole
current_hole = 1

# define hole properties
hole_radius = 30
cup_radius = 33
cup_colour = (60,60,60)
hole_color = (0, 0, 0)
hole_position = np.array([700, 500])

# define the properties for the ball being hit
mouse_power = 0
mouse_max_power = 20
mouse_power_increment = 0.01
mouse_direction = np.array([1, 0])

# define gravity
gravity = np.array([0, 9.8])

dt = 0.1

# define initial ball position and velocity
ball_position = np.array([100, 100])
ball_velocity = np.array([0.0, 0.0])
ball_force = np.array([0.0,0.0])
ball_friction = np.array([0.0,0.0])

# define game loop
running = True

while running:

    # clear the screen
    screen.fill((0, 128, 0))
    screen.blit(grass_file,(0,0))

    # draw the hole
    pygame.draw.circle(screen, cup_colour, hole_position, cup_radius)

    pygame.draw.circle(screen, hole_color, hole_position, hole_radius)
    #draw the sandpits for hole 2
    if(current_hole == 2 or current_hole ==3):
        for sandpit in sandpits:
            pygame.draw.rect(screen, sand_colour, (sandpit["position"],sandpit["size"]))
    # draw the ball
    pygame.draw.circle(screen, ball_color, ball_position.astype(int), ball_radius)

    # calculate distance between ball and hole
    distance = np.linalg.norm(ball_position - hole_position)

    # check if ball is in the hole
    cont = False
    if distance < hole_radius - ball_radius:
        #when the ball enters the hole make sure it stops on the hole
        ball_velocity = np.array([0, 0])
        ball_position = hole_position - np.array([0, hole_radius - ball_radius - distance])
        #print out the strokes it took to 
        print("You completed hole", current_hole, "in:", strokes, "strokes")
        #when hole 3 is completed and the ball is in the hole it exits
        if(current_hole == 3):
            running = False
        #setup new positions for Hole 3
        if(current_hole == 2):
            current_hole = 3
            obstacles[0]["position"] = np.array([150,400])
            obstacles[1]["position"] = np.array([300,450])
            obstacles[2]["position"] = np.array([70,300])
            obstacles[2]["size"] = 60
            obstacles[3]["position"] = np.array([30,200])
            sandpits[0]["position"] = np.array([400,200])
            sandpits[0]["size"] = np.array([200,200])
            hole_position = np.array([75, 550])
            ball_position = np.array([100,100])
            strokes = 0
        #setup new positions for hole 2
        if(current_hole ==1):
            current_hole = 2
            obstacles[0]["position"] = np.array([550,180])
            obstacles[1]["position"] = np.array([700,100])
            obstacles[2]["position"] = np.array([400,300])
            obstacles[3]["position"] = np.array([30,200])
            hole_position = np.array([700, 220])
            ball_position = np.array([100,100])
            strokes = 0
            
    #check if player hits the ball 
    #only want this to hapen once so event.get() is used
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:    
                print("Space pressed")
                strokes +=1
                ball_force= (mouse_power/100) * mouse_direction
                ball_velocity[0] = ball_force[0] / ball_mass 
                ball_velocity[1] = ball_force[1] / ball_mass

        if event.type == pygame.QUIT:
            running = False
    
    #calculate the forces acting on the ball after it has been hit
    ball_friction = - grass_friction_coefficient * ball_velocity 
    ball_velocity = ball_velocity + ball_friction
    ball_position = ball_position + ball_velocity

    force_keyboard = np.array([0, 0])

    #HANDLE THE USER INPUT
    event = pygame.event.get()
    #use w a s d to control the power and direction of the hits
    if pygame.key.get_pressed()[pygame.K_w]:
        if mouse_power < mouse_max_power:
            mouse_power += mouse_power_increment
    if pygame.key.get_pressed()[pygame.K_s]:
        if mouse_power > 0:
            mouse_power -= mouse_power_increment
    if pygame.key.get_pressed()[pygame.K_a]:
        mouse_direction = np.array([np.cos(0.001) * mouse_direction[0] - np.sin(0.001) * mouse_direction[1], 
                                    np.sin(0.001) * mouse_direction[0] + np.cos(0.001) * mouse_direction[1]])
    if pygame.key.get_pressed()[pygame.K_d]:
        mouse_direction = np.array([np.cos(-0.001) * mouse_direction[0] - np.sin(-0.001) * mouse_direction[1], 
                                    np.sin(-0.001) * mouse_direction[0] + np.cos(-0.001) * mouse_direction[1]])

    # ball_velocity = ball_velocity + (force_gravity + force_friction + force_keyboard) / ball_mass

    # handle wall collisions
    if ball_position[0] - ball_radius < 0:
        ball_position[0] = ball_radius
        ball_velocity[0] *= -1
        # ball_position[0] = ball_radius
    elif ball_position[0] + ball_radius > screen_width:
        ball_position[0] = screen_width -ball_radius
        ball_velocity[0] *= -1
        # ball_position[0] = screen_width - ball_radius
    if ball_position[1] - ball_radius < 0:
        ball_position[1] = ball_radius
        ball_velocity[1] *= -1
        # ball_position[1] = ball_radius
    elif ball_position[1] + ball_radius > screen_height:
        ball_position[1] = screen_height - ball_radius
        ball_velocity[1] *= -1
    # draw power bar
    power_bar_length = 200
    power_bar_height = 20
    power_bar_position = np.array([50, 50])
    pygame.draw.rect(screen, (255, 255, 255), (power_bar_position[0], power_bar_position[1], power_bar_length, power_bar_height), 2)
    pygame.draw.rect(screen, (255, 255, 255), (power_bar_position[0], power_bar_position[1], mouse_power * (power_bar_length / mouse_max_power), power_bar_height))

    # draw direction line
    direction_line_length = 50
    direction_line_end = ball_position + direction_line_length * mouse_direction
    pygame.draw.line(screen, (255, 255, 255), ball_position.astype(int), direction_line_end.astype(int))

    #draw score
    font = pygame.font.SysFont("Arial", 18)
    stroke_text = font.render(("Strokes: "), True, (255,255,255))
    stroke_score = font.render(str(strokes), True,(255,255,255))

    screen.blit(stroke_text, (50,10))
    screen.blit(stroke_score, (120,10))
    hole_text = font.render(("Hole: "), True, (255,255,255))
    hole_number = font.render(str(current_hole), True, (255,255,255))
    screen.blit(hole_text, (700,10))
    screen.blit(hole_number, (750,10))

    #draw the obstacles to screen
    for obstacle in obstacles:
        pygame.draw.circle(screen, (128,128,128), (obstacle["position"][0], obstacle["position"][1]), obstacle["radius"])


    # handle collisions for each obstacle
    for obstacle in obstacles:
        pball , rball = ball_position, ball_radius
        pobstacle = obstacle["position"][0] , obstacle["position"][1]
        robstacle = obstacle["radius"]
        dot = np.linalg.norm(pobstacle - ball_position)
        #finding out if the ball and obstacle are coming into contact
        if(dot < rball +robstacle):
            #using large mass for the obstacle because it will not move
            M = ball_mass + 1000
            n = np.linalg.norm(ball_position-pobstacle)**2
            u1 = ball_velocity -2*1000/M *np.dot(ball_velocity, ball_position - pobstacle)/n * (ball_position-pobstacle)
            ball_velocity = u1
    
    #for holes 2 and 3 sandpits are used
    # calculates the new friction when the ball passes over sand
    if(current_hole == 2 or current_hole ==3):
        for sandpit in sandpits: 
            #create outline for rectangle
            r_top = sandpit["position"][1]
            r_right = sandpit["position"][0] + sandpit["size"][0]
            r_bottom = sandpit["position"][1] + sandpit["size"][1]
            r_left = sandpit["position"][0]
            #if the ball is on top of the sand the friction coefficient changes 
            if(r_top <= ball_position[1] <= r_bottom and r_left <=ball_position[0] <= r_right):
                grass_friction_coefficient = 0.023
            else:
                grass_friction_coefficient = 0.0026
    
    pygame.display.update()

pygame.quit()  