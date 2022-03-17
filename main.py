import PySimpleGUI as sg
import hashlib, requests, random, time, json

debug = False

size = (400, 150)


def diceroll():  #based off https://pysimplegui.readthedocs.io/en/latest/#persistent-window-example-running-timer-that-updates
    dice = ["""-----
|   |
| o |
|   |
-----""", """-----
|o  |
|   |
|  o|
-----""", """-----
|o  |
| o |
|  o|
-----""", """-----
|o o|
|   |
|o o|
-----""", """-----
|o o|
| o |
|o o|
-----""", """-----
|o o|
|o o|
|o o|
-----"""]

    sg.SetOptions(element_padding=(0, 0))

    layout = [[
        sg.Text(size=(20, 20),
                font=('DejaVu Sans Mono', 20),
                justification='center',
                key='text')
    ]]

    window = sg.Window('Rolling dice',
                       layout,
                       no_titlebar=True,
                       keep_on_top=True,
                       grab_anywhere=True,
                       size=(250, 180))

    # ----------------  main loop  ----------------
    for x in range(random.randint(10, 70)):
        # --------- Read and update window --------
        event, values = window.read(timeout=10)
        # --------- Display timer in window --------
        dicea = random.choice(dice).split("\n")
        diceb = random.choice(dice).split("\n")
        fulldice = f"{dicea[0]}  {diceb[0]}\n{dicea[1]}  {diceb[1]}\n{dicea[2]}  {diceb[2]}\n{dicea[3]}  {diceb[3]}\n{dicea[4]}  {diceb[4]}\n"
        window['text'].update(fulldice)
        time.sleep(0.05)
    window.close()
    




def dicerollsingle():
    dice = [
        """-----
|   |
| o |
|   |
-----""", """-----
|o  |
|   |
|  o|
-----""", """-----
|o  |
| o |
|  o|
-----""", """-----
|o o|
|   |
|o o|
-----""", """-----
|o o|
| o |
|o o|
-----""", """-----
|o o|
|o o|
|o o|
-----"""
    ]

    sg.SetOptions(element_padding=(0, 0))

    layout = [[
        sg.Text(size=(20, 20),
                font=('DejaVu Sans Mono', 20),
                justification='center',
                key='text')
    ]]

    window = sg.Window('Rolling dice',
                       layout,
                       no_titlebar=True,
                       keep_on_top=True,
                       grab_anywhere=True,
                       size=(130, 180))

    # ----------------  main loop  ----------------
    for x in range(random.randint(10, 70)):
        # --------- Read and update window --------
        event, values = window.read(timeout=10)
        # --------- Display timer in window --------
        window['text'].update(random.choice(dice))
        time.sleep(0.05)
    window.close()


#

#diceroll()


def isEven(number):
    r = requests.get(f"https://api.isevenapi.xyz/api/iseven/{number}/")
    data = r.json()
    return data["iseven"]


#


def readData(file):
    users = []
    hashes = []
    f = open(file, 'r')
    for line in f:
        data = line.split(';')
        users.append(data[0])
        hashes.append(data[1][:-1])
    f.close()
    return (users, hashes)


def debugOut(message):
    global debug
    if debug == True:
        print(f"debug: {message}")


def login(header):
    layout = [[sg.Text(header)], [sg.InputText(key='-UN-')],
              [sg.InputText(key='-PW-', password_char='*')],
              [sg.Button('Log in'), sg.Button('Sign up'), sg.Quit()]]

    window = sg.Window('Dice game', layout, size=size)
    while True:
        event, values = window.read()

        un_input = values['-UN-']
        pw_input = values['-PW-']

        username = un_input
        password = hashlib.sha256(pw_input.encode()).hexdigest()

        if event == "Log in":
            userID = None
            users, hashes = readData('dictionary.txt')
            for i in range(len(users)):
                if users[i] == username and hashes[i] == password:
                    userID = i
            if userID != None:
                Login = userID
                userName = users[userID]
                debugOut("Logged in successfully as User " + str(userID) + ".")
                debugOut("Logged in successfully as " + str(userName) + ".")
                sg.popup("Logged in successfully as " + str(userName) + ".")
                break
            else:
                sg.popup("Could not log in as " + username)
                debugOut("Could not log in as " + username)
                #login(header, user=username)
        elif event == "Sign up":
            debugOut("Sign up")
            repeat = 0
            users, hashes = readData('dictionary.txt')
            debugOut(users)
            debugOut(repeat)
            if username == "":
                repeat = 1
            if pw_input == "":
                repeat = 1
            if username in users:
                repeat = 2
            debugOut(repeat)
            if repeat == 0:
                f = open("dictionary.txt", 'a')
                f.write(username.lower() + ';' + password + '\n')
                f.close()
                debugOut("Signed up successfully as " + username + ".")
                sg.popup("Signed up successfully as " + username +
                         ".\nPlease log in.")
                userName = username
            elif repeat == 1:
                sg.popup("Please enter a valid username and password")
            elif repeat == 2:
                sg.popup("Username already taken")

        else:
            import sys
            sys.exit()
    sg.user_settings_set_entry('-last position-', window.current_location())
    window.close()
    return username


#


def round(score, user):
    layout = []
    tempscore = 0
    dice1 = random.randint(1, 6)
    layout.append([sg.Text(f"Dice 1: {dice1}")])
    debugOut(f"Dice 1: {dice1}")

    dice2 = random.randint(1, 6)
    layout.append([sg.Text(f"Dice 2: {dice2}")])
    debugOut(f"Dice 2: {dice2}")
    tempscore = dice1 + dice2

    if isEven(tempscore):
        tempscore += 10
        debugOut("You get a bonus score of 10!")
        layout.append([
            sg.Text(
                f"Because your total is even, you get a bonus score of 10!")
        ])
    else:
        tempscore -= 5
        debugOut("You get a bonus score of -5!")
        layout.append([
            sg.Text(f"Because your total is odd, you get a bonus score of -5!")
        ])

    if dice1 == dice2:
        sg.popup_auto_close("You rolled a double, so you get a third dice")
        dicerollsingle()
        dice3 = random.randint(1, 6)
        tempscore += dice3
        layout.append([sg.Text(f"Dice 3: {dice3}")])

    score = score + tempscore
    player = scores[f"user{user}"]
    debugOut(f"This round {player} earnt: {tempscore}")
    layout.append([sg.Text(f"This round you earnt: {tempscore}")])

    if score < 0:
        score = 0

    layout.append([sg.Text(f"Your total score is {score}")])

    layout.append([sg.Button('Continue')])

    
    window = sg.Window(f"{player} score",
                       layout,
                       size=size,
                       element_justification='c')
    event, values = window.read()

    return score


#


roundNo = 0
user1 = login("User 1 login")
user2 = login("User 2 login")

scores = {"user1": user1, "score1": 0, "user2": user2, "score2": 0}

while roundNo < 5:
    #temp = input(f"{user1} press enter to roll")
    #sg.popup("Click to roll".center(80, " "))

    layout = [[sg.Text(user1)], [sg.Text('Click to roll')],
              [sg.Button('Roll')]]

    window = sg.Window(f"Round {roundNo+1}",
                       layout,
                       size=size,
                       element_justification='c')
    event, values = window.read()

    diceroll()

    scores["score1"] = round(scores["score1"], 1)
    score1 = scores["score1"]

    #temp = input(f"{user2} press enter to roll")
    #sg.popup("Click to roll")

    layout = [[sg.Text(user2)], [sg.Text('Click to roll')],
              [sg.Button('Roll')]]

    window = sg.Window(f"Round {roundNo+1}",
                       layout,
                       size=size,
                       element_justification='c')
    event, values = window.read()

    diceroll()

    scores["score2"] = round(scores["score2"], 2)
    score2 = scores["score2"]
    roundNo += 1

#scores["score1"], scores["score2"] = 50, 51

score1 = scores["score1"]
score2 = scores["score2"]

if score1 == score2:
    #tie breaker
    def tiebreaker():
        sg.popup_auto_close("Sudden Death!")
        layout = [[sg.Text(user1)], [sg.Text('Click to roll')],
                  [sg.Button('Roll')]]
        window = sg.Window("Sudden Death!",
                           layout,
                           size=size,
                           element_justification='c')
        user1SuddenDeathScore = random.randint(1, 6)
        debugOut(user1SuddenDeathScore)
        event, values = window.read()

        dicerollsingle()

        layout = [[sg.Text(user2)], [sg.Text('Click to roll')],
                  [sg.Button('Roll')]]
        window = sg.Window("Sudden Death!",
                           layout,
                           size=size,
                           element_justification='c')
        event, values = window.read()

        dicerollsingle()

        user2SuddenDeathScore = random.randint(1, 6)
        debugOut(user2SuddenDeathScore)
        if user1SuddenDeathScore == user2SuddenDeathScore:
            return tiebreaker()
        else:
            return user1SuddenDeathScore, user2SuddenDeathScore

    user1SuddenDeathScore, user2SuddenDeathScore = tiebreaker()

    scores["score1"] = scores["score1"] + user1SuddenDeathScore
    scores["score2"] = scores["score2"] + user2SuddenDeathScore

    score1 = scores["score1"]
    score2 = scores["score2"]
    debugOut(score1)
    debugOut(score2)

layout = [[sg.Text(f"{user1} scored a total of: {score1}")],
          [sg.Text(f"{user2} scored a total of: {score2}")],
          [sg.Button("Finish")], 
          [sg.Button("View global leaderboard")]]

if score1 > score2:
    layout.insert(
        0, [sg.Text(f"{user1} wins! They scored {score1-score2} more!")])
else:
    layout.insert(
        0, [sg.Text(f"{user2} wins! They scored {score2-score1} more!")])

window = sg.Window(f"Results",
                   layout,
                   size=size,
                   element_justification='c')
event, values = window.read()


with open("scores.json", "r") as f:
    globalScores = json.loads(f.read())
    try:
        if globalScores[user1] < score1:
            globalScores[user1] = score1
    except:
        globalScores[user1] = score1
    try:
        if globalScores[user2] < score2:
            globalScores[user2] = score2
    except:
        globalScores[user2] = score2


with open("scores.json", "w") as f:
    f.write(json.dumps(globalScores))
    
with open("scores.json", "r") as f:
    debugOut(f.read())



if event == "View global leaderboard":
    highest = []
    glob = globalScores
    debugOut(glob)
    for key in glob:
        if len(highest) < 6 or glob[key] > highest[:-1][0]:
            highest.append([glob[key], key])

        highest.sort()

        if len(highest) > 5:
            highest.pop(0)
    if len(highest) < 5:
        while len(highest) < 5:
            highest.append([0, "..."])
            highest.sort()
    debugOut(highest)
    
    
    layout = [[sg.Text("".join(["1st place".ljust(12, " "), highest[4][1].ljust(16, " "), str(globalScores[highest[4][1]]).ljust(4, " ")]), font=('DejaVu Sans Mono', 10))],
              [sg.Text("".join(["2nd place".ljust(12, " "), highest[3][1].ljust(16, " "), str(globalScores[highest[3][1]]).ljust(4, " ")]), font=('DejaVu Sans Mono', 10))],
              [sg.Text("".join(["3rd place".ljust(12, " "), highest[2][1].ljust(16, " "), str(globalScores[highest[2][1]]).ljust(4, " ")]), font=('DejaVu Sans Mono', 10))],
              [sg.Text("".join(["4th place".ljust(12, " "), highest[1][1].ljust(16, " "), str(globalScores[highest[1][1]]).ljust(4, " ")]), font=('DejaVu Sans Mono', 10))],
              [sg.Text("".join(["5th place".ljust(12, " "), highest[0][1].ljust(16, " "), str(globalScores[highest[0][1]]).ljust(4, " ")]), font=('DejaVu Sans Mono', 10))]]

    window = sg.Window("Global Leaderboard", layout, size=size,                        element_justification='l')
    event, values = window.read()

window.close()