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

def GetResult(type:str, revealedDoors:list, chosenDoor:int, roomDict:dict):
    if type == "switch":
        finalDoor = list(set(roomDict.keys()) - set(revealedDoors))
        finalDoor.remove(chosenDoor)
        finalDoor = int(finalDoor[0])
    elif type == "stay":
        finalDoor = chosenDoor
    else:
        print("Error. Type is not Switch or Stay. [GetResult]")
    return tuple([roomDict[finalDoor] == 1, finalDoor, type])

def UserSimulation(doorNum:int):
    print("Look up the info for Manual Simulation to know how to play.")
    roundNum = 0
    allFirstChoices = []
    allActions = []
    allResults = []
    while True:
        roundNum += 1
        print("-"*20)
        cprint("Round #"+str(roundNum), "green")
        roomDict = GenerateRoom(doorNum, doorNum-numberOfGoodDoors)
        chosenDoor = int(PrintFunctions.LimitedInput(list(roomDict.keys()), "Pick a door", " | "))
        doorsToBeRevealed = RevealDoor(chosenDoor, roomDict)
        print()
        if len(doorsToBeRevealed) > 10:
            for i in range(1, len(roomDict)+1):
                if i not in doorsToBeRevealed and i != chosenDoor:
                    print(f"Door {i} may be the prize door.\n")
                    break
        elif len(doorsToBeRevealed) == 1:
            print(f"Goat is in door {doorsToBeRevealed[0]}\n")
        else:
            print("Goats are in doors:", end=" ")
            for i in doorsToBeRevealed:
                if not i == doorsToBeRevealed[-1]:
                    print(i, end=", ")
                else:
                    print(str(i)+".\n")
        result, finalDoor, action = GetResult(PrintFunctions.LimitedInput(["stay", "switch"], f"Do you want to stay or switch:"), doorsToBeRevealed, chosenDoor, roomDict)
        if action == "stay":
            print(f"\nYou stayed with Door {finalDoor}")
        elif action == "switch":
            print(f"\nYou switched to Door {finalDoor}")
        if result:
            cprint(f"Door {finalDoor} has the Prize! You Win!", "green")
        else:
            cprint(f"Door {finalDoor} had the Goat. Too Bad.", "red")
            print(f"The car is in Door {list(roomDict.keys())[list(roomDict.values()).index(1)]}")
        
        allFirstChoices.append(chosenDoor)
        allActions.append(action.capitalize())
        allResults.append("Win" if result else "Lose")
        
        print()
        if PrintFunctions.LimitedInput(["y", "n"], "Do you want to play again:") == "n":
            break
    print("")
    PrintResults(list(i+1 for i in range(roundNum)), allFirstChoices, allActions, allResults, roundNum, extendedResults)

def SilentSimulations(doorNum:int, simulationTimes:int, simType:str="random choices", runningDefaultSim:bool=False, fileSave:str=""):
    if simType == "always stay": actionRandomChoice = "stay"
    elif simType == "always switch": actionRandomChoice = "switch"
    print(f"Simulating for {simulationTimes} times, with {doorNum} doors. The action is {simType}.")
    print('Progress: 0.0%'+'\r', end="")
    allFirstChoices = []
    allActions = []
    allResults = []
    allRounds = list(i+1 for i in range(simulationTimes))
    for r in allRounds:
        roomDict = GenerateRoom(doorNum, doorNum-numberOfGoodDoors)
        chosenDoor = random.choice(list(roomDict.keys()))
        doorsToBeRevealed = RevealDoor(chosenDoor, roomDict)
        if simType == "random choices": actionRandomChoice = random.choice(["stay", "switch"])
        result, finalDoor, action = GetResult(actionRandomChoice, doorsToBeRevealed, chosenDoor, roomDict)
        allFirstChoices.append(chosenDoor)
        allActions.append(action.capitalize())
        allResults.append("Win" if result else "Lose")
        print(f'Progress: {round(r/simulationTimes*100, 2)}%'+'\r', end="")
    print("\n")
    if fileSave != "":
        SaveToFile(fileSave, allRounds, allFirstChoices, allActions, allResults, simulationTimes)
    if not runningDefaultSim:
        if simulationTimes <= 100:
            PrintResults(allRounds, allFirstChoices, allActions, allResults, simulationTimes, extendedResults)
        else:
            print("The table was not printed because it was too long.\n")
            PrintResults(allRounds, allFirstChoices, allActions, allResults, simulationTimes, extendedResults, False)
        return
    return allActions, allResults, allFirstChoices

def RunDefaultSilentSimulations(simType, amountOfDoors, saveToFile = True, fileName=""):
    simulationTimes = [50, 100, 1000, 5000, 10000]
    allActions, allResults, allFirstChoices = [], [], []
    for sim in simulationTimes:
        if sim == 1000 and saveToFile:
            actions, results, choices = SilentSimulations(amountOfDoors, sim, simType, True, fileName)
        else:
            actions, results, choices = SilentSimulations(amountOfDoors, sim, simType, True)
        allActions += actions
        allResults += results
        allFirstChoices += choices
    PrintFunctions.PrintTable([list(i+1 for i in range(50)), allFirstChoices[:50], allActions[:50], allResults[:50]], 50, tableTitle="50 ROUND RESULTS TABLE")
    print("\nThe rest were simulated silently...\n")

    stayPrs, switchPrs = [], []
    for i in range(len(simulationTimes)):
        if not i == 0: before = simulationTimes[i-1]
        else: before = 0
        current = simulationTimes[i]
        roundActions = allActions[before+1:current+before+1]
        roundResults = allResults[before+1:current+before+1]
        switchWins, stayWins, switchCount, stayCount = 0, 0, 0, 0
        for s in range(len(roundActions)):
            if roundResults[s] == "Win":
                if roundActions[s] == "Stay":
                    stayWins += 1
                    stayCount += 1
                else:
                    switchWins += 1
                    switchCount += 1
            else:
                if roundActions[s] == "Stay":
                    stayCount += 1
                else:
                    switchCount += 1
        stayPrs.append(str(round(stayWins/stayCount*100,2))+"%")
        switchPrs.append(str(round(switchWins/switchCount*100,2))+"%")

    PrintFunctions.PrintTable([simulationTimes, switchPrs, stayPrs], 5, "SILENT SIMULATION RESULTS", ["Rounds", "Pr(Win with Switch)", "Pr(Win with Stay)"])

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