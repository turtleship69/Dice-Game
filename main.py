import PySimpleGUI as sg
import hashlib, requests, random

def isEven(number):
    r = requests.get(f"https://api.isevenapi.xyz/api/iseven/{number}/")
    data = r.json()
    return data["iseven"]

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
debug = True


def login(header, user=""):

    layout = [
        [sg.Text(header)],
        [sg.InputText(key='-UN-')],
        [sg.InputText(key='-PW-', password_char='*')],
        [sg.Button('Log in'), sg.Button('Sign up'),sg.Quit()]
    ]

    window = sg.Window('Dice game', layout)

    #event, values = window.read()

    #window['-UN-'].update(user)
    while True:

        event, values = window.read()

        #window.close()

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
                sg.popup("Logged in successfully as User " + str(userID) + ".")
                break
            else:
                sg.popup("Could not log in as " + username)
                debugOut("Could not log in as " + username) 
                #login(header, user=username)
        elif event == "Sign up":
            users, hashes = readData('dictionary.txt')
            debugOut(users)
            if username != "" and password != "":
                f = open("dictionary.txt", 'a')
                f.write(username.lower() + ';' + password + '\n')
                f.close()
                debugOut("Signed up successfully as " + username + ".")
                sg.popup("Signed up successfully as " + username + ".")
                userName = username

        else:
            import sys
            sys.exit()

    window.close()
    return username


def round():
    tempscore = 0
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    tempscore = dice1 + dice2
    if isEven(tempscore):
        tempscore += 5
    



user1 = login("Player 1 log in or sign up")
user2 = login("Player 2 log in or sign up")
#while user2 == user1:
#    sg.popup("Unacceptable")
#    user2 = login("Player 2 log in")

round = 0

#while round < 5:
    