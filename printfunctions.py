from termcolor import colored, cprint
import sys

def LimitedInput(choices:list=["y","n"], prompt="Pick an option:", promptseperator=", ", promptcolour="yellow", promptattrs:list=["bold"], error="Invalid. Please try again.", errorcolour="red", errorattrs:list=[]):
    for i in range(len(choices)):
        choices[i] = str(choices[i])
    cprint(prompt, promptcolour, attrs=promptattrs)
    cprint("Options:", end=" ", attrs=["bold"])
    for i in range(len(choices)):
        if i == len(choices) - 1:
            print(str(choices[i]))
        else:
            print(str(choices[i]), end=promptseperator)
    numberChoices = []
    for i in range(len(choices)):
        numberChoices.append(str(i+1))
    while True:
        answer = input(": ").lower()
        valid = True
        if answer not in choices:
            valid = False
        if answer in numberChoices:
            answer = choices[int(answer)-1]
            valid = True
        if answer in ["q", "quit"]:
            valid = False
            sys.exit()
        if valid:
            break
        else:
            cprint(error, errorcolour, attrs=errorattrs)
    return answer

def ListedInput(choices:dict={"y": "yes", "n": "no"}, prompt="Pick an option:", choiceseperator=" | ", error="Invalid. Please try again.", returnKey:bool=False):
    cprint(prompt, "yellow", attrs=["bold"])
    for i in range(len(choices.keys())):
        print(str(list(choices.keys())[i])+choiceseperator+str(choices[list(choices.keys())[i]]))
    valuesList = list(choices.values())
    for i in range(len(valuesList)):
        valuesList[i] = str(valuesList[i]).lower()
    numberChoices = []
    for i in range(len(choices.keys())):
        numberChoices.append(str(i+1))
    while True:
        answer = input(": ").lower()
        valid = True
        if answer not in choices.keys():
            valid = False
        if answer in valuesList:
            valid = True
            answerIndex = valuesList.index(answer)
            answer = list(choices.keys())[answerIndex]
        if answer in numberChoices:
            answer = list(choices.keys())[int(answer)-1]
            valid = True
        if answer in ["q", "quit"]:
            valid = False
            cprint("Selected Quit Program", "green")
            sys.exit()
        if valid:
            break
        else:
            cprint(error, "red", attrs=["bold"])
    keyAnswer = answer
    answer = choices[answer]
    cprint(f"Selected {answer}\n", "green")
    if returnKey:
        return keyAnswer
    else:
        return answer

def RangedInput(start:int, end:int, prompt="Choose a number:", error="Invalid. Please try again.", infiniteEnd:bool=False):
    if infiniteEnd:
        end = "∞"
    cprint(prompt, "yellow", attrs=["bold"])
    while True:
        answer = input(f"Pick between {start} to {end}: ")
        if answer == "q" or answer == "quit":
            cprint("Selected Quit Program", "green")
            sys.exit()
        try:
            answer = int(answer)
        except:
            cprint(error, "red", attrs=["bold"])
            continue
        valid = True
        if infiniteEnd:
            if answer < start:
                valid = False
        else:
            if answer < start or answer > end:
                valid = False
        if answer in ["q", "quit"]:
            valid = False
            sys.exit()
        if valid:
            break
        else:
            cprint(error, "red", attrs=["bold"])
    cprint("Selected "+str(answer), "green")
    return answer

def PrintTable(data:list[list], tableLength:int, tableTitle:str="RESULTS TABLE", titles:list=["Round", "Choice", "Action", "Outcome"], tableBuffer:int=2):
    longestString = 0
    data.append(titles)
    for lists in data:
        for value in lists:
            if len(str(value)) > longestString:
                longestString = len(str(value))
    data.remove(titles)
    cprint(tableTitle, attrs=["bold"])
    print("")
    for title in titles:
        print(colored(title, attrs=["underline"]), end=" "*(longestString-len(str(title))+tableBuffer))
    print("")
    for i in range(tableLength):
        for l in data:
            try:
                value = l[i]
            except IndexError:
                value = ""
            print(str(value), end=" "*(longestString-len(str(value))+tableBuffer))
        print("")
    print("")
