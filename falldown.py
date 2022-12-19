#Kevin Lam, mvk2uy
import uvage
import random

camera = uvage.Camera(600, 750)

#player gamebox
character = uvage.from_color(200, 300, "white", 20, 20)

#structures
list_of_floors = []
left_wall = uvage.from_color(0, 0, "black", 5, 2000)
right_wall = uvage.from_color(600, 0, "black", 5, 2000)

#falling speeds
box_base = 3
box_falling_velocity = box_base
gravity = 1.1

#game setting
game_over = False
game_on = False
score = 0
first_start = True




# ------ Move the box / detect collision with walls ------
def move_character():
    """
    this moves the character and detects the wall collisions
    :return: nothing, used to move
    """
    if uvage.is_pressing("left arrow"):

        if character.touches(left_wall):
            character.x = 0
        else:
            character.x -= 10
    if uvage.is_pressing("right arrow"):
        if not character.touches(right_wall):
            character.x += 10

# ----- Box falling with and without touching the floors -----
def character_touches_floor():
    """
    takes in the global variables to calculate the speed of falling depending if it hits the floors or not
    :return:
    """
    global box_base
    global gravity
    global box_falling_velocity
    box_touching = False
    for floor in list_of_floors:
        for half in floor:
            if character.bottom_touches(half):
                character.move_to_stop_overlapping(half)
                box_touching = True

    if box_touching == True:
        character.y -= 5
        box_falling_velocity = box_base
    else:
        if character.y <= 730:
            box_falling_velocity *= gravity
            character.y += box_falling_velocity






# ----- Make the Floors ------
def making_floors(y=0):
    """
    makes the floors
    :param y: the height of where the floor will be drawn
    :return: list of the floors
    """

    global list_of_floors #list of 2 halves of a floor within a list of floors
    list_of_sides_floors = []
    for floor in range(8): # initially makes 8 floors
        list_of_sides_floors = [] #list of 2 halves
        width_left = random.randint(25,500) #random chooses width of left side
        width_right = 550 - width_left # uses the left width to make width of right side
        list_of_sides_floors.append(uvage.from_color(width_left//2 , y, "black", width_left, 15)) #appending left half to list_of_sides_floors, width_left//2 to find center point of the floor to spawn
        list_of_sides_floors.append(uvage.from_color(width_left+50 + width_right//2, y, "black", width_right, 15)) #appending right half
        list_of_floors.append(list_of_sides_floors) #appends the list of sides to list of floors
        y += 140 # gap between each floor


# ------ Move the floors and make new floors when playing -------
def move_floors():
    """
    moves the floors up at a constant speed
    :return: movement of floors
    """
    for floor in list_of_floors: #for each floor, there will be two halves that each need to move up at the same speed
        for half in floor:
            half.y -= 5
    if list_of_floors[1][0].y < 0: # when the second to top floor reaches the top of screen, done here because it needs to take in consideration of moving floors so condition can be met
        del list_of_floors[0] #deletes the first floor to reduce useless data
        list_of_sides_floors = [] # doing the floor creation again in making_floor function
        width_left = random.randint(25, 500)
        width_right = 550 - width_left
        list_of_sides_floors.append(uvage.from_color(width_left // 2, 980, "black", width_left, 15)) # done 140 pixels under the 8th floor in the making_floor function
        list_of_sides_floors.append(uvage.from_color(width_left + 50 + width_right // 2, 980, "black", width_right, 15))
        list_of_floors.append(list_of_sides_floors)




making_floors() #calling function to make floors

#run the game
def tick():
    """
    this processes the function and game
    :return: the game
    """
    global game_on
    global game_over
    global character
    global score
    global first_start

    if uvage.is_pressing("space"):
        game_on= True

    if game_on: #games starting

        # ------ Box functions -------
        move_character()


        # ----- Floor functions ------
        character_touches_floor()
        move_floors()

        # ---- Keeping Score ----
        score += 1

    # ----- Draw stuff -----

    camera.clear("light green") #green background and clears the lagging end of the box
    camera.draw(character)

    for floor in list_of_floors: #draws each half
        for half in floor:
            camera.draw(half)

    camera.draw(left_wall)
    camera.draw(right_wall)

    camera.draw(uvage.from_text(300, 50, str(score//30), 50, "Red", bold=True)) #scoreboard, divide by 30 because of 30 ticks per second

    if not game_on and first_start: # for the message of how to start the game, only appears during the first start

        camera.draw(uvage.from_text(300, 200, "Press Space to Start", 50, "Red", bold=True))


    if character.y < -10: #reaches the top, loses
        game_on = False
        game_over = True

    if game_over == True: # shows game over texts when player loses
        camera.draw(uvage.from_text(300, 200, "GAME OVER", 50, "Red", bold=True))
        game_on = False
        first_start = False #turns off the first start message

    camera.display()

uvage.timer_loop(30, tick)
