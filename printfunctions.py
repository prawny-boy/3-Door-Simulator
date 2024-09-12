from termcolor import colored, cprint
import sys

def LimitedInput(choices:list=["y","n"], prompt="Pick an option:", promptseperator=", ", promptcolour="yellow", promptattrs:list=["bold"], error="Invalid. Please try again.", errorcolour="red", errorattrs:list=[]):
    for i in range(len(choices)):
        choices[i] = str(choices[i])
    cprint(prompt, promptcolour, attrs=promptattrs)
    cprint("Options:", end=" ", attrs=["bold"])
    for i in range(len(choices)):
        if i == len(choices) - 1:
            print(str(choices[i])+".")
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