# Name: Jason Heo Jung
# Class: P05
# Date: 9/8/2021
# Program description: PRG Assignment

# import libraries
import random
import pickle

# initialise

# deletes blanks on the highscore board to prevent too many blanks
for v in range(10):
    leader_file = open("leaderboard.txt", "a")
    leader_file.write(str(0) + "," + "blank" + "\n")
    leader_file.close()
with open("leaderboard.txt", "r") as f:
    lines = f.readlines()
with open("leaderboard.txt", "w") as f:
    for line in lines:
        if line.strip("\n") != "0,blank":
            f.write(line)
# adds blanks to the highscore board to fill it
for v in range(10):
    leader_file = open("leaderboard.txt", "a")
    leader_file.write(str(0) + "," + "blank" + "\n")
    leader_file.close()

# different building types
building_types = ["HSE", "BCH", "SHP", "FAC", "HWY"]

# list of positions as to where buildings can be placed so that their adjacent
can_put = []


# functions


# menu() prints the main menu
def menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Show high scores")
    print('\n0. Exit')
    choice = str(input('Your choice? '))
    # returns the user input
    return choice


# map() prints a new map
def game_map(map_data, buildings_type, buildings_list):
    z = 0
    print("    ", end="")
    for g in range(len(map_data[0])):
        # prints characters above map
        print("{:6}".format(chr(65 + g)), end="")
    # prints remaining buildings
    print("{:>18}{:>20}".format("Buildings", "Remaining"))
    # prints map
    print(" +-----", end="")
    for i in range(len(map_data[0]) - 1):
        print("+-----", end="")
        if i == len(map_data[0]) - 2:
            print("+", end="")
    print("{:>20}{:>20}".format("---------", "---------"))
    for j in range(len(map_data[0])):
        print(j + 1, end="")
        for i in range(len(map_data[0])):
            print("| {}".format(map_data[j][i][0]), end=' ')
        if j <= 2:
            print("|", end=" ")
        if j > 2:
            print("|")
        if z < 5:
            print("{:>19}{:>20}".format(buildings_type[z], buildings_list.count(buildings_type[z])))
            z += 1
        elif z > 5:
            print("")
        print(" +-----", end="")
        for m in range(len(map_data[0]) - 1):
            print("+-----", end="")
        if j <= 1:
            print("+", end="")
        if j > 1:
            print("+")
        if z < 5:
            print("{:>20}{:>20}".format(buildings_type[z], buildings_list.count(buildings_type[z])))
            z += 1
        elif z > 5:
            print("")


# selects random buildings from the building list
def random_buildings(building_list):
    why = 0
    while why == 0:
        no1 = random.randint(0, len(building_list) - 1)
        no2 = random.randint(0, len(building_list) - 1)
        while no1 == no2:
            no2 = random.randint(0, len(building_list) - 1)
        check1 = building_list.count(building_list[no1])
        check2 = building_list.count(building_list[no2])
        if check1 != 0 or check2 != 0:
            building_1 = building_list[no1]
            building_2 = building_list[no2]
            why += 1
        else:
            continue
        # returns random buildings
        return building_1, building_2


# game_menu prints a game menu
def game_menu(building_1, building_2):
    print("1. Build a", building_1)
    print("2. Build a", building_2)
    print("3. See current score")
    print("\n4. Save game")
    print("0. Exit to main menu")
    choice = str(input("Your Choice? "))
    # returns choice and the buildings in the options
    return choice, building_1, building_2


# Places building that is in option 1 on the map
def option_1(map_data, building_1, building_2, building_list, turn_num):
    U = 0
    X = 0
    Y = 0
    a = 0
    while a == 0:
        try:
            # finds location on the map and replaces it with building
            location = str(input("Build where? "))
            U = location.upper()
            X = int(ord(U[0])) - 65
            Y = int(U[1]) - 1
            V = map_data[Y][X].count("   ")  # checks if the coordinate is available
            if V == 1:  # if coordinate is available
                map_data[Y][X].append(str(building_1))
                map_data[Y][X].remove("   ")
                building_list.remove(building_2)
                building_list.remove(building_1)
                a = 1  # breaks loop
            elif V == 0:  # if coordinate is not available
                print("Buildings cannot overlap each other")
                continue  # continues loop
        except:
            print("Please enter a valid choice")
    return U, X, Y, building_1, building_2, turn_num, building_list


# Places building that is in option 2 on the map
def option_2(map_data, building_1, building_2, building_list, turn_num):
    U = 0
    X = 0
    Y = 0
    a = 0
    while a == 0:
        try:
            # finds location on the map and replaces it with building
            location = str(input("Build where? "))
            U = str(location.upper())
            X = int(ord(U[0])) - 65
            Y = int(U[1]) - 1
            V = map_data[Y][X].count("   ")  # checks if the coordinate is available
            if V == 1:  # if coordinate is available
                map_data[Y][X].append(str(building_2))
                map_data[Y][X].remove("   ")
                building_list.remove(building_2)
                building_list.remove(building_1)
                a = 1  # breaks loop
            elif V == 0:  # if coordinate is not available
                print("Buildings cannot overlap each other")
                continue  # continues loop
        except:
            print("Please enter a valid choice")
    return U, X, Y, building_1, building_2, turn_num, building_list


# makes sure that buildings are adjacent to each other
def adjacent(map_data, u, x, y, building, spare_building, turn_num, building_list, build1, build2):
    # adds coordinates where buildings can be placed
    usable1 = int(ord(u[0])) + 1
    use_1 = chr(usable1)
    using1 = u.replace(u[0], use_1)
    can_put.append(using1)
    usable2 = int(ord(u[0])) - 1
    use_2 = chr(usable2)
    using2 = u.replace(u[0], use_2)
    can_put.append(using2)
    usable3 = int(u[1]) + 1
    usable3_1 = str(usable3)
    using3 = u.replace(u[1], usable3_1)
    can_put.append(using3)
    usable4 = int(u[1]) - 1
    usable4_1 = str(usable4)
    using4 = u.replace(u[1], usable4_1)
    can_put.append(using4)
    # if user tries to print a building that is not in the list of available spots...
    if u not in can_put:
        # replaces the coordinate back with a blank instead of the building
        map_data[y][x].append("   ")
        map_data[y][x].remove(building)
        print("You must build next to an existing building.")
        building_list.append(spare_building)
        building_list.append(building)
        # removes the spots added when attempting to add the building not in the list
        can_put.remove(using1)
        can_put.remove(using2)
        can_put.remove(using3)
        can_put.remove(using4)
        turn_num -= 1  # turn number decreases
        return turn_num, build1, build2
    else:
        build1, build2 = random_buildings(buildings)
        return turn_num, build1, build2


# Displays scoreboard
def scoreboard(map_data):
    print("HSE:", end=" ")
    # initialise
    house_tallying = []
    house_list = []
    house_score_list = []
    house_scored = 0
    house_score_total = 0
    # scans the map for HSE
    for h in range(len(map_data[0])):
        for s in range(len(map_data[0])):
            houses = map_data[h][s].count("HSE")
            house_list.append(houses)
            # if HSE is found
            if houses == 1:
                house_score = 0
                # checks to see if the coordinate adjacent to the house is not a border
                if h - 1 < 0:
                    house_score = 0
                    house_tallying.append(house_score)
                elif h - 1 >= 0:
                    # checks above the HSE
                    x = map_data[h - 1][s][0]
                    # if its a HSE, score 1 point
                    if x == "HSE":
                        house_score = house_score + 1
                    # if its a SHP, score 1 point
                    if x == "SHP":
                        house_score = house_score + 1
                    # if its a BCH, score 2 point
                    if x == "BCH":
                        house_score = house_score + 2
                    # if its a FAC, score will be 1 point
                    if x == "FAC":
                        house_tallying.clear()
                        house_score = 1
                        house_score_list.append(house_score)
                        continue
                    house_tallying.append(house_score)
                # checks to see if the coordinate adjacent to the house is not a border
                if h + 1 > len(map_data[0]) - 1:
                    house_score = 0
                    house_tallying.append(house_score)
                elif h + 1 <= len(map_data[0]) - 1:
                    # checks below the HSE
                    y = map_data[h + 1][s][0]
                    house_score = 0
                    # if its a HSE, score 1 point
                    if y == "HSE":
                        house_score = house_score + 1
                    # if its a SHP, score 1 point
                    if y == "SHP":
                        house_score = house_score + 1
                    # if its a BCH, score 2 point
                    if y == "BCH":
                        house_score = house_score + 2
                    # if its a FAC, score will be 1 point
                    if y == "FAC":
                        house_tallying.clear()
                        house_score = 1
                        house_score_list.append(house_score)
                        continue
                    house_tallying.append(house_score)
                # checks to see if the coordinate adjacent to the house is not a border
                if s - 1 < 0:
                    house_score = 0
                    house_tallying.append(house_score)
                elif s - 1 >= 0:
                    # checks the left of the coordinate
                    z = map_data[h][s - 1][0]
                    house_score = 0
                    # if its a HSE, scores 1 point
                    if z == "HSE":
                        house_score = house_score + 1
                    # if its a SHP, scores 1 point
                    if z == "SHP":
                        house_score = house_score + 1
                    # if its a BCH, scores 2 point
                    if z == "BCH":
                        house_score = house_score + 2
                    # if its a FAC, score will be 1 point
                    if z == "FAC":
                        house_tallying.clear()
                        house_score = 1
                        house_score_list.append(house_score)
                        continue
                    house_tallying.append(house_score)

                if s + 1 > len(map_data[0]) - 1:
                    house_score = 0
                    house_tallying.append(house_score)
                elif s + 1 <= len(map_data[0]) - 1:
                    # checks the right of the coordinate
                    p = map_data[h][s + 1][0]
                    house_score = 0
                    # if its a HSE, scores 1 point
                    if p == "HSE":
                        house_score = house_score + 1
                    # if its a SHP, scores 1 point
                    if p == "SHP":
                        house_score = house_score + 1
                    # if its a BCH, score 2 point
                    if p == "BCH":
                        house_score = house_score + 2
                    # if its a FAC, score will be 1 point
                    if p == "FAC":
                        house_tallying.clear()
                        house_score = 1
                        house_score_list.append(house_score)
                        continue
                    house_tallying.append(house_score)  # adds the points accumulated by the house to a list
                # adds up the points to get the score of the house
                for i in range(len(house_tallying)):
                    house_scored = house_scored + house_tallying[i]
                house_score_list.append(house_scored)  # puts the score of the house in a list
                # resets the list and values
                house_tallying = []
                house_scored = 0
            else:
                continue
    # prints out the scores of the houses
    if len(house_score_list) == 0:
        print("0")
    elif len(house_score_list) > 0:
        for j in range(len(house_score_list)):
            house_score_total += house_score_list[j]
        for m in range(len(house_score_list)):
            if m < len(house_score_list) - 1:
                print(house_score_list[m], end=" + ")
            if m == len(house_score_list) - 1:
                print(house_score_list[m], "=", house_score_total)

    # prints out factory score
    print("FAC:", end=" ")
    factory_list = []
    factory_score = 0
    for w in range(len(map_data[0])):
        for e in range(len(map_data[0])):
            factories = map_data[w][e].count("FAC")
            factory_list.append(factories)
    factory_count = factory_list.count(1)  # counts number of factories in the map
    if factory_count == 0:  # if there is no factory score is 0
        print("0")
        factory_score = 0
    elif factory_count == 1:  # if there is 1 factory score of factory is 1
        print("1", end=" ")
        factory_score = factory_count * 1
        print("=", factory_score)
    elif factory_count == 2:  # if there is 2 factories score of factories is 2 each
        print("2 + 2", end=" ")
        factory_score = factory_count * 2
        print("=", factory_score)
    elif factory_count == 3:  # if there is 3 factories score of factories is 3 each
        print("3 + 3 + 3", end=" ")
        factory_score = factory_count * 3
        print("=", factory_score)
    elif factory_count == 4:  # if there is 4 factories score of factories is 4 each
        print("4 + 4 + 4 + 4", end=" ")
        factory_score = factory_count * 4
        print("=", factory_score)
    elif factory_count > 4:  # if there is more than 4 factories, the first 4 scores of factories is 4 each, rest are 1
        print("4 + 4 + 4 + 4", end=" ")
        factory_remaining = factory_count - 4
        for x in range(factory_remaining):
            print("+ 1", end=' ')
        print("=", factory_score)  # prints final score

    # prints out shop score
    print("SHP:", end=" ")
    shop_score_list = []
    shop_score_total = 0
    for d in range(len(map_data[0])):
        for x in range(len(map_data[0])):
            shops = map_data[d][x].count("SHP")  # finds shops in the map
            if shops == 1:
                shop_score = 0
                shop_building_list = ["HSE", "FAC", "SHP", "HWY", "BCH"]
                # checks above the SHP
                if d - 1 < 0:
                    shop_score += 0
                if d - 1 >= 0:
                    y = map_data[d - 1][x][0]
                    if y in shop_building_list:  # if building is in the list it scores 1 point
                        shop_score += 1
                        shop_building_list.remove(y)
                # checks below the SHP
                if d + 1 > 3:
                    shop_score += 0
                if d + 1 <= 3:
                    y = map_data[d + 1][x][0]
                    if y in shop_building_list:  # if building is in the list it scores 1 point
                        shop_score += 1
                        shop_building_list.remove(y)
                # checks left of the SHP
                if x - 1 < 0:
                    shop_score += 0
                if x - 1 >= 0:
                    y = map_data[d][x - 1][0]
                    if y in shop_building_list:  # if building is in the list it scores 1 point
                        shop_score += 1
                        shop_building_list.remove(y)
                # checks right of the SHP
                if x + 1 > 3:
                    shop_score += 0
                if x + 1 <= 3:
                    y = map_data[d][x + 1][0]
                    if y in shop_building_list:  # if building is in the list it scores 1 point
                        shop_score += 1
                        shop_building_list.remove(y)
                shop_score_list.append(shop_score)
    # prints shop scores and total
    if len(shop_score_list) == 0:
        print("0")
    for n in range(len(shop_score_list)):
        shop_score_total += shop_score_list[n]
    for o in range(len(shop_score_list)):
        if o < len(shop_score_list) - 1:
            print(shop_score_list[o], end=" + ")
        if o == len(shop_score_list) - 1:
            print(shop_score_list[o], "=", shop_score_total)

    # prints out highway score
    print("HWY:", end=" ")
    highway_score_list = []
    highway_score_total = 0
    for z in range(len(map_data[0])):
        highway_list = []
        for f in range(len(map_data[0])):
            highways = map_data[z][f][0].count("HWY")  # scans map for highways
            if highways == 1:
                highway_list.append(highways)  # if highway found, finds how many are placed horizontally in a row
            elif highways == 0:
                for a in range(len(highway_list)):
                    if len(highway_list) == 1:  # if highway only has 1 in a row, score 1
                        highway_score = highway_list[a] * 1
                        highway_score_list.append(highway_score)
                    elif len(highway_list) == 2:  # if highway has 2 in a row, score 2 each
                        highway_score = highway_list[a] * 2
                        highway_score_list.append(highway_score)
                    elif len(highway_list) == 3:  # if highway has 3 in a row, score 3 each
                        highway_score = highway_list[a] * 3
                        highway_score_list.append(highway_score)
                    elif len(highway_list) == 4:  # if highway has 4 in a row, score 4 each
                        highway_score = highway_list[a] * 4
                        highway_score_list.append(highway_score)
                    else:
                        continue
                highway_list = []
        for a in range(len(highway_list)):
            if len(highway_list) == 1:  # if highway only has 1 in a row, score 1
                highway_score = highway_list[a] * 1
                highway_score_list.append(highway_score)
            elif len(highway_list) == 2:  # if highway has 2 in a row, score 2 each
                highway_score = highway_list[a] * 2
                highway_score_list.append(highway_score)
            elif len(highway_list) == 3:  # if highway has 3 in a row, score 3 each
                highway_score = highway_list[a] * 3
                highway_score_list.append(highway_score)
            elif len(highway_list) == 4:  # if highway has 4 in a row, score 4 each
                highway_score = highway_list[a] * 4
                highway_score_list.append(highway_score)
            else:
                continue

    # scores of highways are added into a list and printed
    if len(highway_score_list) == 0:
        print("0")
    for b in range(len(highway_score_list)):
        highway_score_total += highway_score_list[b]
        if highway_score_list[b] == 0:
            continue
        if b < len(highway_score_list) - 1:
            print(highway_score_list[b], end=" + ")
        elif b == len(highway_score_list) - 1:
            print(highway_score_list[b], "=", highway_score_total)

    # Prints out the beach score
    print("BCH:", end=" ")
    side_beach_list = []
    beach_list = []
    for i in range(len(map_data[0])):
        for h in range(len(map_data[0])):
            beaches = map_data[i][h].count("BCH")  # Checks for total number of beaches on the map
            beach_list.append(beaches)
        beaches_sideA = map_data[i][0].count("BCH")
        side_beach_list.append(beaches_sideA)  # Checks and accounts for total number of beaches on side A
        beaches_sideB = map_data[i][len(map_data[0]) - 1].count("BCH")
        side_beach_list.append(beaches_sideB)  # Checks and accounts for total number of beaches on side B
    side_beaches = side_beach_list.count(1)
    beaches = beach_list.count(1)  # Finds total number of beaches
    individual_beaches = beaches - side_beaches  # Finds beaches that are not on the sides
    if side_beaches > 0:  # prints score for side beaches
        for b in range(side_beaches):
            if b < side_beaches - 1:
                print("3", end=" + ")
            else:
                print("3", end=" ")
    if individual_beaches > 0:  # prints score for beaches not at side
        print("+", end=" ")
    for q in range(individual_beaches):
        if q < individual_beaches - 1:
            print("1", end=" + ")
        else:
            print("1", end=" ")
    beach_score = individual_beaches + side_beaches * 3
    if side_beaches > 0 or individual_beaches > 0:
        print("=", beach_score)
    if side_beaches == 0 and individual_beaches == 0:
        print("0")

    # prints total score
    print("Total score: ", end="")
    total_score = beach_score + highway_score_total + shop_score_total + factory_score + house_score_total
    print(total_score)
    return total_score


# saves the game
def save(s, d, f, g, h, j):
    # Writes the required variables into a file
    turn_num = open("turns.txt", "w")
    turn_num.write(s)
    turn_num.close()
    with open("mapdata.txt", "wb") as fp:
        pickle.dump(d, fp)
    with open("adjacent.txt", "wb") as fp:
        pickle.dump(f, fp)
    with open("buildings.txt", "wb") as fp:
        pickle.dump(g, fp)
    building1txt = open("building1.txt", "w")
    building1txt.write(h)
    building1txt.close()
    building2txt = open("building2.txt", "w")
    building2txt.write(j)
    building2txt.close()
    print("Game has been saved")


# loads a saved game
def load():
    # Reads all the required variables to load the saved game
    turn = open("turns.txt", "r")
    saved_turn = turn.read()
    turn.close()
    with open("mapdata.txt", "rb") as fp:
        saved_map_data = pickle.load(fp)
    with open("adjacent.txt", "rb") as fp:
        adjacent_list = pickle.load(fp)
    with open("buildings.txt", "rb") as fp:
        buildings_left = pickle.load(fp)
    build1 = open("building1.txt", "r")
    save_building1 = build1.read()
    build1.close()
    build2 = open("building2.txt", "r")
    save_building2 = build2.read()
    build2.close()
    return saved_turn, saved_map_data, adjacent_list, buildings_left, save_building1, save_building2


# Exits the game
def exit_game():
    exit()


# prints the leaderboard
def leaderboard():
    leaderboard_file = open("leaderboard.txt", "r")
    file_read = leaderboard_file.readlines()
    sorted_file = sorted(file_read, reverse=True)  # makes the leaderboard organized on who has the highest score
    # prints the actual leaderboard
    print("--------- HIGH SCORES ---------")
    print("{:4}{:22}{}".format("Pos", "Player", "Score"))
    print("--- ------                -----")
    for lines in range(10):
        p = str(sorted_file[lines]).split(",")
        p[1] = p[1].replace("\n", "")
        print("{:4}{:25}{}".format(str(lines + 1) + ".", str(p[1]), str(p[0])))
    print("-------------------------------")


# updates highscore board when a user reaches into the highscore board
def score_entered(score):
    # reads file and sorts it by highest score
    leaderboard_file = open("leaderboard.txt", "r")
    file_read = leaderboard_file.readlines()
    sorted_file = sorted(file_read, reverse=True)
    leaderboard_file.close()
    # checks if users score applies for the highscore board
    for i in range(10):
        p = str(sorted_file[i]).split(",")
        p[1] = p[1].replace("\n", "")
        if score > int(p[0]):  # If they make it they are prompted to enter their name
            print("Congratulations! You made the high score board at position ", i + 1, "!")
            name = str(input("Please enter your name (max 20 chars): "))
            leaderboard_file = open("leaderboard.txt", "a")
            leaderboard_file.write(str(score) + "," + name + "\n")
            leaderboard_file.close()
            break
    # prints out the highscore board
    leaderboard()


# Main Program
while True:
    # map data
    rows = [[['   '], ['   '], ['   '], ['   ']],
            [['   '], ['   '], ['   '], ['   ']],
            [['   '], ['   '], ['   '], ['   ']],
            [['   '], ['   '], ['   '], ['   ']]]

    # buildings list
    buildings = ["HSE", "HSE", "HSE", "HSE", "HSE", "HSE", "HSE", "HSE",
                 "BCH", "BCH", "BCH", "BCH", "BCH", "BCH", "BCH", "BCH",
                 "SHP", "SHP", "SHP", "SHP", "SHP", "SHP", "SHP", "SHP",
                 "FAC", "FAC", "FAC", "FAC", "FAC", "FAC", "FAC", "FAC",
                 "HWY", "HWY", "HWY", "HWY", "HWY", "HWY", "HWY", "HWY"]

    # list of positions as to where buildings can be placed so that their adjacent
    can_put = []
    print('Welcome, mayor of Simp City!')
    print('----------------------------')
    userChoice = menu()
    if userChoice == '1':
        turns = 1
        building1, building2 = random_buildings(buildings)
        while turns <= 16:  # loops until its greater than 16
            print("Turn", turns)
            game_map(rows, building_types, buildings)  # prints game map
            game_choice, building_x, building_y = game_menu(building1, building2)  # prints game menu
            if game_choice == '1':  # when user puts 1 option 1 is selected
                building_location, letter, number, building_type, other_building, turns, buildings =\
                    option_1(rows, building_x, building_y, buildings, turns)
                if turns == 1:
                    can_put.append(building_location)  # allows building to be placed anywhere when its turn 1
                # checks to make sure buildings are adjacent
                turns, building1, building2 = adjacent(rows, building_location, letter, number, building_type,
                                                       other_building, turns, buildings, building1, building2)
            elif game_choice == '2':  # when user puts 2 option 2 is selected
                building_location, letter, number, other_building, building_type, turns, buildings = \
                    option_2(rows, building_x, building_y, buildings, turns)
                if turns == 1:
                    can_put.append(building_location)  # allows building to be placed anywhere when its turn 1
                # checks to make sure buildings are adjacent
                turns, building1, building2 = adjacent(rows, building_location, letter, number, building_type,
                                                       other_building, turns, buildings, building1, building2)
            elif game_choice == '3':  # when user puts 3 scores are displayed
                scoreboard(rows)
                turns -= 1
            elif game_choice == '4':  # when users put 4 game is saved
                save(str(turns), rows, can_put, buildings, building1, building2)
                turns -= 1
            elif game_choice == '0':  # when user puts 0 game exits out of loop and returns to the menu
                break
            # if user does not give any valid option they are looped back and prompted to enter a valid choice
            elif game_choice != '1' or '2' or '3' or '4' or '5' or '0':
                print("Please enter a valid choice")
                turns -= 1
            if turns == 16:  # after the last turn, final layout is printed as well as high score board
                print("Final layout of Simp City:")
                game_map(rows, building_types, buildings)
                final_score = scoreboard(rows)
                score_entered(final_score)
            turns += 1

    # loading from save file
    elif userChoice == '2':
        try:
            # save file is loaded
            saved_turns, saved_rows, can_put, saved_buildings, saved_building1, saved_building2 = load()
            saved_turns = int(saved_turns)
        except:
            # if an error occurs the user is prompted to make sure they have a save file
            print("Please ensure you have a save file")
            continue
        while saved_turns <= 16:  # loops until turns reach 16
            print("Turn", saved_turns)
            game_map(saved_rows, building_types, saved_buildings)  # prints game map
            game_choice, building_x, building_y = game_menu(saved_building1, saved_building2)  # game menu is printed
            if game_choice == '1':  # if user chooses option 1
                building_location, letter, number, building_type, other_building, saved_turns, saved_buildings = \
                    option_1(saved_rows, building_x, building_y, saved_buildings, saved_turns)
                if saved_turns == 1:
                    can_put.append(building_location)  # allows building to be placed anywhere when its turn 1
                    # checks to make sure buildings are adjacent
                saved_turns, saved_building1, saved_building2 = adjacent(saved_rows, building_location, letter, number,
                                                                         building_type, other_building,
                                                                         saved_turns, saved_buildings, saved_building1,
                                                                         saved_building2)
            elif game_choice == '2':
                building_location, letter, number, other_building, building_type, saved_turns, saved_buildings = \
                    option_2(saved_rows, building_x, building_y, saved_buildings, saved_turns)
                if saved_turns == 1:
                    can_put.append(building_location)  # allows building to be placed anywhere when its turn 1
                # checks to make sure buildings are adjacent
                saved_turns, saved_building1, saved_building2 = adjacent(saved_rows, building_location, letter, number,
                                                                         building_type, other_building,
                                                                         saved_turns, saved_buildings, saved_building1,
                                                                         saved_building2)
            elif game_choice == '3':  # if user chooses 3 scores is printed
                scoreboard(saved_rows)
                saved_turns -= 1
            elif game_choice == '4':  # if user chooses 4 game is saved
                save(str(saved_turns), saved_rows, can_put, saved_buildings, saved_building1, saved_building2)
                saved_turns -= 1
            elif game_choice == '0':  # if user choose 0 the loop is broken and they are back at the main menu
                break
            else:
                saved_turns -= 1
                print("Please enter a valid choice")  # user is prompted for a valid
            if saved_turns == 16:
                print("Final layout of Simp City:")  # once turns has reached the end it prints out final layout
                game_map(saved_rows, building_types, saved_buildings)
                final_score = scoreboard(saved_rows)
                score_entered(final_score)
            saved_turns += 1
    elif userChoice == '3':  # if user chooses 3, high score board is shown
        leaderboard()
    elif userChoice == '0':  # if user chooses 0 they exit the program
        exit_game()
    else:
        print("Please enter a valid choice")
        continue
