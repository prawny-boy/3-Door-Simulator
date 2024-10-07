import random # to randomly generate chosen doors and actions for silent sims
import sys # to quit the code
sys.dont_write_bytecode = True # this makes sure pycache doesnt generate
import PrintFunctions # a different file with printing functions like tables and user error
from termcolor import cprint # colour printing

# Variables - These are just set now to be used later
numberOfGoodDoors = 1
unknownDoorAmount = 2
amountOfDoors = 3
maximumAmountOfDoors = 100
extendedResults = False
roundCount = 0
doorFirstChoices = []
actions = []
outcomes = []

# Functions
def GenerateRoom(doorNum:int, goatCount:int): # this generates a room dictionary with doors that have cars (1) or goats (0)
    doorDict = {i+1:0 for i in range(doorNum)} # make a dictionary with doors 1 to x with 0 as values
    doorList = list(doorDict.keys()) # make a list of the doors (just numbers 1 to x)
    for _ in range(doorNum-goatCount): # loops the amount of car doors times
        goodDoor = random.choice(doorList) # choose a random door
        doorDict[goodDoor] = 1 # change the value of that door to 1 (car door)
        doorList.remove(goodDoor) # remove the car door from the list
    return doorDict # returns the doors with the goat or car on each (dict)

def RevealDoor(chosenDoor:int, roomDict:dict): # this reveals x minus 2 doors that have goats
    revealableDoors = list(roomDict.keys()) # makes a list of all the doors
    revealableDoors.remove(chosenDoor) # removes the chosen door from the list
    if roomDict[chosenDoor] != 1: # if the chosen door is not a car
        revealableDoors.remove(list(roomDict.keys())[list(roomDict.values()).index(1)]) # removes the car door
    else: # if it is a car
        revealableDoors.remove(random.choice(revealableDoors)) # picks a random door to remove
    doorsRevealed = sorted(revealableDoors) # sorts the doors to be revealed
    return doorsRevealed # returns the revealed doors

def GetResult(type:str, revealedDoors:list, chosenDoor:int, roomDict:dict): # this gets the result of the simulation depending on switch or stay
    if type == "switch": # if it is switch
        finalDoor = list(set(roomDict.keys()) - set(revealedDoors)) # removes the revealed doors from the list of doors
        finalDoor.remove(chosenDoor) # removes the chosen door to get the door that the user switched to
        finalDoor = int(finalDoor[0]) # sets this door to the finaldoor variable
    elif type == "stay": # if it is stay
        finalDoor = chosenDoor # then set the final door to the current chosen door because it doesnt change
    else:
        print("Error. Type is not Switch or Stay. [GetResult]") # error message if it is not switch or stay
    return tuple([roomDict[finalDoor] == 1, finalDoor, type]) # returns the result (true/false) depending if the final door is == 1 (or it is the win door) and also the actualy final door, and the switch or stay

def UserSimulation(doorNum:int): # simulates using functions above for interactive with user
    print("Look up the info for Manual Simulation to know how to play.")
    roundNum = 0 # sets round number to 0, this will increase as the user plays the simulation
    allFirstChoices = [] # defining lists for results later
    allActions = []
    allResults = []
    while True: # loop until the player wants to stop
        roundNum += 1 # changes the round number by 1
        print("-"*20)
        cprint("Round #"+str(roundNum), "green") # prints the round number to the user
        roomDict = GenerateRoom(doorNum, doorNum-numberOfGoodDoors) # generates the doors etc using the function
        chosenDoor = int(PrintFunctions.LimitedInput(list(roomDict.keys()), "Pick a door", " | ")) # sets the chosen door to the input of the user
        doorsToBeRevealed = RevealDoor(chosenDoor, roomDict) # reveals door(s) to the user
        print()
        if len(doorsToBeRevealed) > 10: # if the length of the reveal door list (from the revealdoor function) is bigger than 10
            for i in range(1, len(roomDict)+1): # this chunk of code just prints it as the remaining door, instead of al the revealed doors (if there is lots of doors being simulated)
                if i not in doorsToBeRevealed and i != chosenDoor:
                    print(f"Door {i} may be the prize door.\n")
                    break
        elif len(doorsToBeRevealed) == 1: # if there is only one revealed door, or there are 3 doors being simulated
            print(f"Goat is in door {doorsToBeRevealed[0]}\n") # prints the revealed door
        else: # otherwise (2-9 revealed doors)
            print("Goats are in doors:", end=" ") # this chunk of code just prints all the revealed goat doors seperated in commas
            for i in doorsToBeRevealed:
                if not i == doorsToBeRevealed[-1]:
                    print(i, end=", ")
                else:
                    print(str(i)+".\n")
        result, finalDoor, action = GetResult(PrintFunctions.LimitedInput(["stay", "switch"], f"Do you want to stay or switch:"), doorsToBeRevealed, chosenDoor, roomDict) # this gets the user input to stay or switch and puts it in the getresult function to calculate the win or lose
        if action == "stay": # if the user stayed
            print(f"\nYou stayed with Door {finalDoor}") # prints that the user stayed in the final door
        elif action == "switch": # if the user switched
            print(f"\nYou switched to Door {finalDoor}") # prints that the user switched in the final door
        if result: # tells the user if they won or lost
            cprint(f"Door {finalDoor} has the Prize! You Win!", "green") # win
        else:
            cprint(f"Door {finalDoor} had the Goat. Too Bad.", "red") # lose
            print(f"The car is in Door {list(roomDict.keys())[list(roomDict.values()).index(1)]}") # prints the prize door
        
        allFirstChoices.append(chosenDoor) # appends the round results to the list to print later in the table (this is the chosen door at the start)
        allActions.append(action.capitalize()) # stay or switch
        allResults.append("Win" if result else "Lose") # win or lose
        
        print()
        if PrintFunctions.LimitedInput(["y", "n"], "Do you want to play again:") == "n": # asks if the user wants to play again
            break # if no, break from the while true loop to print results
    print("")
    PrintResults(list(i+1 for i in range(roundNum)), allFirstChoices, allActions, allResults, roundNum, extendedResults) # prints a table with the results of the interactive simulation

def SilentSimulations(doorNum:int, simulationTimes:int, simType:str="random choices", runningDefaultSim:bool=False, fileSave:str=""): # This function handles silent simulation, taking 5 parameters: doorNum, simulationTimes, simType, runningDefaultSim, fileSave
    if simType == "always stay": actionRandomChoice = "stay" # if the simulation type passed into the function is always stay, change it to stay for easier use
    elif simType == "always switch": actionRandomChoice = "switch" # if it is always switch, change it to switch for easier use
    print(f"Simulating for {simulationTimes} times, with {doorNum} doors. The action is {simType}.") # prints what the simualtion is simulating
    print('Progress: 0.0%'+'\r', end="") # starts the progress bar at 0 percent
    allFirstChoices = [] # list of all first choices for table
    allActions = [] # list of all actions
    allResults = [] # list of all results
    allRounds = list(i+1 for i in range(simulationTimes)) # list of all rounds 1,2,3,4...
    for r in allRounds: # for each round in the list of rounds
        roomDict = GenerateRoom(doorNum, doorNum-numberOfGoodDoors) # generate the room dictionary
        chosenDoor = random.choice(list(roomDict.keys()))  # pick a random door to be chosen
        doorsToBeRevealed = RevealDoor(chosenDoor, roomDict) # reveals doors silently
        if simType == "random choices": actionRandomChoice = random.choice(["stay", "switch"]) # stays or switches depending on the mode, if it is random, use random.choice to pick
        result, finalDoor, action = GetResult(actionRandomChoice, doorsToBeRevealed, chosenDoor, roomDict) # get the final results of the round
        allFirstChoices.append(chosenDoor) # appends the round results to the list to print later in the table
        allActions.append(action.capitalize()) # stay or switch
        allResults.append("Win" if result else "Lose") # win or lose
        print(f'Progress: {round(r/simulationTimes*100, 2)}%'+'\r', end="") # updates the progress bar to loop again after
    print("\n")
    if fileSave != "": # if the user wants to save the results (not filesave is equal to empty string)
        SaveToFile(fileSave, allRounds, allFirstChoices, allActions, allResults, simulationTimes) # save the file using the function
    if not runningDefaultSim: # if the user is not running the default simulation (the 100, 1000, 5000, 10000 simulations)
        if simulationTimes <= 100: # if the simulation times is less than or equal to 100 (because table cant be too long)
            PrintResults(allRounds, allFirstChoices, allActions, allResults, simulationTimes, extendedResults) # print the results
        else:
            print("The table was not printed because it was too long.\n") # print that the table is too long to print
            PrintResults(allRounds, allFirstChoices, allActions, allResults, simulationTimes, extendedResults, False) # just print the results not including the table (see false in the function)
        return # ends the function by calling return
    return allActions, allResults, allFirstChoices # returns the actions, results, and first choices to be printed in the default sim function

def RunDefaultSilentSimulations(simType, amountOfDoors, saveToFile = True, fileName=""): # This function runs the default silent simulations for 50, 100, 1000, 10000 rounds
    simulationTimes = [50, 100, 1000, 5000, 10000] # list of simulation times
    allActions, allResults, allFirstChoices = [], [], [] # list of all actions, results, and first choices
    for sim in simulationTimes: # for each simulation time count in the list
        if sim == 1000 and saveToFile: # if the simulation count is equal to 1000 and the user wants to save
            actions, results, choices = SilentSimulations(amountOfDoors, sim, simType, True, fileName) # silent simulation with saving
        else:
            actions, results, choices = SilentSimulations(amountOfDoors, sim, simType, True) # silent simulation without saving (no filename)
        allActions += actions # adds the actions
        allResults += results # adds the results
        allFirstChoices += choices # adds the first choices
    PrintFunctions.PrintTable([list(i+1 for i in range(50)), allFirstChoices[:50], allActions[:50], allResults[:50]], 50, tableTitle="50 ROUND RESULTS TABLE") # prints the table with the 50 round
    print("\nThe rest were simulated silently...\n") # prints that the rest were simulated silently

    stayPrs, switchPrs = [], [] # makes lists of stay and switch percentages
    for i in range(len(simulationTimes)): # for each simulation time
        if not i == 0: before = simulationTimes[i-1] # if it is not the first simulation before sets to the previous simulation
        else: before = 0 # if it is the first simulation before sets to 0
        current = simulationTimes[i] # sets to the current simulation times
        roundActions = allActions[before+1:current+before+1] # checks the actions of the round
        roundResults = allResults[before+1:current+before+1] # checks the results of the round
        switchWins, stayWins, switchCount, stayCount = 0, 0, 0, 0 # sets switch wins, stay wins, switch count, and stay count to 0
        for s in range(len(roundActions)): # for each round
            if roundResults[s] == "Win": # if the result is win
                if roundActions[s] == "Stay": # if the action is stay
                    stayWins += 1 # adds to stay wins
                    stayCount += 1 # adds to stay count
                else: # if the action is switch
                    switchWins += 1 # adds to switch wins
                    switchCount += 1 # adds to switch count
            else: # if the result is lose
                if roundActions[s] == "Stay": # if the action is stay
                    stayCount += 1 # adds to stay count
                else: # if the action is switch
                    switchCount += 1 # adds to switch count
        
        if switchCount == 0: # resolving zero division error with if statements
            winningWithSwitch = 0.0
        else:
            winningWithSwitch = round(switchWins/switchCount*100, 2)
        if stayCount == 0:
            winningWithStay = 0.0
        else:
            winningWithStay = round(stayWins/stayCount*100, 2)
        
        stayPrs.append(str(winningWithStay)+"%") # prints the results
        switchPrs.append(str(winningWithSwitch)+"%")

    PrintFunctions.PrintTable([simulationTimes, switchPrs, stayPrs], 5, "SILENT SIMULATION RESULTS", ["Rounds", "Pr(Win with Switch)", "Pr(Win with Stay)"]) # prints the 50, 100, 1000, 10000 round table with probabilities

def SilentSimulationMenu():
    print("Check info on types of Silent Simulation if you are struggling to understand.")
    silentSimType = PrintFunctions.ListedInput({"d": "Defaults", "c": "Customise"}, "Select the type of Silent Simulation:").lower()
    if silentSimType == "customise":
        print("You can customise the doors and the amount of simulations.")

        simType = str(PrintFunctions.ListedInput({"1": "Random Choices", "2": "Always Switch", "3": "Always Stay"}, "Pick type of silent simulation: (1/3 Type)")).lower()
        amountOfSims = str(PrintFunctions.ListedInput({"1": "Controlled (50, 100, 1000, 5000, 10000 times)", "2": "Custom Amount"}, "Pick type of silent simulation: (2/3 Simulation Times)", returnKey=True)).lower()
        if amountOfSims == "2":
            amountOfSims = PrintFunctions.RangedInput(1, 1, "Pick amount of Simulation Times:", infiniteEnd=True)
        amountOfDoors = str(PrintFunctions.ListedInput({"1": "Default (3)", "2": "Many Doors (10)", "3": "Custom"}, "Pick type of silent simulation: (3/3 Door Amount)", returnKey=True)).lower()
        if amountOfDoors == "3":
            amountOfDoors = PrintFunctions.RangedInput(1, 1, "Pick amount of Doors:", infiniteEnd=True)
        elif amountOfDoors == "2": amountOfDoors = 10
        elif amountOfDoors == "1": amountOfDoors = 3
        if amountOfSims == "1":
            RunDefaultSilentSimulations(simType, amountOfDoors)
        else:
            SilentSimulations(amountOfDoors, amountOfSims, simType)
    elif silentSimType == "defaults":
        print("All are simulated with 50, 100, 1000, 5000, 10000 rounds. Files are saved if you desire so.")
        presetSim = PrintFunctions.ListedInput({"1": "Random Stay/Switch", "2": "Always Stay", "3": "Always Switch", "4": "Many Doors"}, "Pick the simulation you want:", choiceseperator=". ", returnKey=True).lower()
        saveFile = PrintFunctions.ListedInput({"y": "Yes", "n": "No"}, "Do you want to save the files?", returnKey=True).lower()
        if saveFile == "y": saveFile = True
        else: saveFile = False
        if presetSim == "1":
            RunDefaultSilentSimulations("random choices", 3, saveFile, "part2_random.txt")
        elif presetSim == "2":
            RunDefaultSilentSimulations("always stay", 3, saveFile, "part3_stay.txt")
        elif presetSim == "3":
            RunDefaultSilentSimulations("always switch", 3, saveFile, "part4_switch.txt")
        elif presetSim == "4":
            RunDefaultSilentSimulations("always switch", 10, saveFile, "part5_ten_doors.txt")

def PrintResults(allRounds:list, allFirstChoices:list, allActions:list, allResults:list, amountOfRounds:int, extendedInfo:bool=False, table:bool=True):
    if table:
        tableData = [allRounds, allFirstChoices, allActions, allResults]
        PrintFunctions.PrintTable(tableData, amountOfRounds)
    winsCount = allResults.count("Win")
    lossesCount = allResults.count("Lose")
    stayCount = allActions.count("Stay")
    switchCount = allActions.count("Switch")
    switchWinCount, switchLossCount, stayWinCount, stayLossCount = 0, 0, 0, 0
    for i in range(amountOfRounds):
        if allActions[i] == "Switch":
            if allResults[i] == "Win":
                switchWinCount += 1
            else:
                switchLossCount += 1
        elif allActions[i] == "Stay":
            if allResults[i] == "Win":
                stayWinCount += 1
            else:
                stayLossCount += 1
    
    if switchCount == 0:
        winningWithSwitch = 0.0
        losingWithSwitch = 0.0
    else:
        winningWithSwitch = round(switchWinCount/switchCount*100, 2)
        losingWithSwitch = round(switchLossCount/switchCount*100, 2)
    if stayCount == 0:
        winningWithStay = 0.0
        losingWithStay = 0.0
    else:
        winningWithStay = round(stayWinCount/stayCount*100, 2)
        losingWithStay = round(stayLossCount/stayCount*100, 2)

    cprint("SUMMARY\n", attrs=["bold"])
    cprint(f"Wins with switch: {switchWinCount}")
    cprint(f"Wins with stay: {stayWinCount}\n")
    print(f"Pr(Winning with switch): {winningWithSwitch}%")
    print(f"Pr(Winning with stay): {winningWithStay}%\n")

    if extendedInfo:
        cprint("EXTENDED INFO\n", attrs=["bold"])
        print(f"Wins: {winsCount}")
        print(f"Losses: {lossesCount}")
        print(f"Pr(Winning): {round(winsCount/amountOfRounds*100, 2)}%")
        print(f"Pr(Losing): {round(lossesCount/amountOfRounds*100, 2)}%\n")
        print(f"Losses with switch: {switchLossCount}")
        print(f"Losses with stay: {stayLossCount}")
        print(f"Pr(Losing with switch): {losingWithSwitch}%")
        print(f"Pr(Losing with stay): {losingWithStay}%\n")
        print(f"Rounds with switch: {switchCount}")
        print(f"Rounds with stay: {stayCount}")
        print(f"Pr(Winning with switch/all rounds): {round(switchWinCount/amountOfRounds*100, 2)}%")
        print(f"Pr(Winning with stay/all rounds): {round(stayWinCount/amountOfRounds*100, 2)}%")
        print(f"Pr(Losing with switch/all rounds): {round(switchLossCount/amountOfRounds*100, 2)}%")
        print(f"Pr(Losing with stay/all rounds): {round(stayLossCount/amountOfRounds*100, 2)}%\n")

def SaveToFile(fileName:str, allRounds:list, allFirstChoices:list, allActions:list, allResults:list, amountOfRounds:int):
    with open(fileName, "w") as file:
        file.truncate()
        file.write("Round,First Choice,Action,Result\n")
        for i in range(amountOfRounds):
            file.write(f"{allRounds[i]},{allFirstChoices[i]},{allActions[i]},{allResults[i]}\n")

def SilentFileUpdate():
    SilentSimulations(3, 1000, "random choices", True, "part2_random.txt")
    SilentSimulations(3, 1000, "always stay", True, "part3_stay.txt")
    SilentSimulations(3, 1000, "always switch", True, "part4_switch.txt")
    SilentSimulations(10, 1000, "random choices", True, "part5_ten_doors.txt")
    print("Files Saved Successfully!\n")

# Main Code
print("-------------------------------------------------------------------")
cprint("The 3-door Problem/Monty Hall Problem Simulator", attrs=["bold", "underline"])
cprint("By Sean Chan", attrs=["bold"])
cprint("Disclaimer: This was made for a school project. Do not take seriously.")
print("-------------------------------------------------------------------\n")
while True:
    command = None
    command = str(PrintFunctions.ListedInput({"p": "Play", "c": "Customisation", "h": "How To Play"}, "Enter a command:")).lower()
    if command == "play":
        command = str(PrintFunctions.ListedInput({"i": "Interactive Simulation", "s": "Silent Simulation", "f": "Update Files", "p": "Previous"}, "Pick type of simulation:")).lower()
        if command == "interactive simulation":
            amountOfDoors = PrintFunctions.RangedInput(3, maximumAmountOfDoors, "Enter amount of doors: (Recommended: 3)")
            UserSimulation(amountOfDoors)
        elif command == "silent simulation":
            SilentSimulationMenu()
        elif command == "update files":
            SilentFileUpdate()
        elif command == "previous":
            continue
    elif command == "customisation":
        while True:
            command = str(PrintFunctions.ListedInput({"c": "Clear files", "e": "Toggle Extended Results", "p": "Previous"}, "Enter a setting to edit:")).lower()
            if command == "clear files":
                files = ["part2_random.txt", "part3_stay.txt", "part4_switch.txt", "part5_ten_doors.txt"]
                for file in files:
                    with open(file, "w") as f: f.truncate()
                cprint("Files cleared successfully.\n", "green")
            elif command == "toggle extended results":
                extendedResults = not extendedResults
                cprint("Extended Info is now set to " + str(extendedResults) + ".\n", "green")
            elif command == "previous":
                break
    elif command == "how to play":
        while True:
            command = str(PrintFunctions.ListedInput({"i": "Interactive Simulations", "s": "Silent Simulations", "p": "Previous"}, "Enter a command:")).lower()
            if command == "previous":
                break
            elif command == "interactive simulations":
                cprint("INTERACTIVE SIMULATION HELP\n", attrs=["bold"])
                print("""Accessing the Interactive Simulation in the Program:
1. Select "Play" from the main menu.
2. Select "Interactive Simulation" from the play menu.
3. Enter the amount of doors you want. (Recommended: 3)

How To Play:
At the start, there are x amount of doors, with each door being numbered 1 to x. One door has a car in it, and the rest have something bad - Goats. The aim is to select the door with the car. You first start by selecting a door, and then the host will reveal x-2 doors that have goats in them. You then can decide to switch to the remaining door, or stay with your current door. Depending what you choose, you can win or lose. Just select 'y' to play again in the program.

When you are done, select 'n' in play again and the results will be printed with statistics. See if you can find a pattern...\n""")
            elif command == "silent simulations":
                cprint("SILENT SIMULATION HELP\n", attrs=["bold"])
                print("""Accessing the Silent Simulation in the Program:
1. Select "Play" from the main menu.
2. Select "Silent Simulation" from the play menu.
3. Enter the type of simulation you want.
        Random Choices means that it will select randomly to do switch or stay.
        Always stay or switch just does what it specifies, always.
4. Enter the amount of times you want to simulate.
        Controlled simulation simulates 100, 500, 1000, 5000, 10000 times and prints a special results table.
        If you customise, it will ask you how many times you want.
5. Enter the amount of doors you want to simulate with.
        Default is 3 door, Many Doors is 10 doors.
        If you customise, it will ask you how many doors you want to simulate with.

The program will then simulate the setting silently and then print results.\n""")