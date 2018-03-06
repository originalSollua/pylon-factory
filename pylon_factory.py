import os
import sys
import time
import datetime
import re
import errno
import random
from socket import error as socket_error
from slackclient import SlackClient
import websocket
import genFact

#activate a slackbot instance
#slackbot userid
botid = None

#constants
RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
CONTINUE_RUNNING = True
RETURN_CODE = 0
CON_T = 0
DIE_RANGE = range(1,100)
DEFAULT_RESPONSE = "You are a goober."
LOG_FN = "log.txt"
LOG_STREAM =[]

def roll(message_text):
    num_dice = 0
    dice_size = 0
    dice_array = []
    LOG_STREAM.append(message_text)
    roll_com = message_text.split(" ")
    if roll_com[0] != "roll":
        return "I dont even know what happened"
    roll_nums  = roll_com[1].split("d")

    # Check if the values are integers
    try:
        num_dice  = int(roll_nums[0])
        dice_size = int(roll_nums[1])
    except TypeError:
        return "Invalid roll parameters. Please use (1-99)d(1-99)"

    # Check if in range, then generate values
    if (num_dice in DIE_RANGE and dice_size in DIE_RANGE):
        for x in range(num_dice):
            dice_array.append(random.randint(1,dice_size))
        output = "You rolled: " + ", ".join(map(str,dice_array))
        output += "\nYour total: " + str(sum(dice_array))
        return output
    else:
        return "Invalid roll parameters. Please use (1-99)d(1-99)"

def iWannaKnow():
    tfact = genFact.get()
    LOG_STREAM.append(tfact)
    return tfact

def connect():
    LOG_STREAM.append("attempting connect")
    with open('.env','r') as env_file:
        bot_token = env_file.readline().rstrip().split("=")[1]
    LOG_STREAM.append(bot_token)
    global slack_client
    slack_client = SlackClient(bot_token)

def writeLog():
    with open(LOG_FN,'a') as logfile:
        for x in LOG_STREAM:
            try:
                logfile.write(str(datetime.datetime.now()) +": "+x)
            except TypeError:
                logfile.write(str(datetime.datetime.now()) +": LOG ERR")
            logfile.write("\n")
    logfile.close()
    del LOG_STREAM[:]



def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_dm(event["text"])
            if user_id == botid:
                LOG_STREAM.append(message)
                return message, event["channel"]
    return None, None

def parse_dm(message_text):
    LOG_STREAM.append(message_text)
    global CON_T
    CON_T = CON_T+1
    if CON_T >= 10:
        chime_in();
        CON_T = 0

    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def chime_in():
    send_message(genFact.get(), "general");


def send_message(message, channel):
    slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text = message or DEFAULT_RESPONSE
            )
    return

def handle_command(command, channel):
    response = None
    if command.startswith("hi"):
        response = "I'M PYLON RIIIIIIIICKKKKK!!!!"

    elif command.startswith("roll"):
        response = roll(command)
        send_message(response, channel)

    elif command.startswith("factoid"):
            response = iWannaKnow()
            send_message(response, channel);

    elif command.startswith("update"):
        global CONTINUE_RUNNING
        global RETURN_CODE
        #added stuff here
        response = "You thought you could shut me down that easily?"
        send_message(response, channel)
        time.sleep(3)
        response = "Just kidding.... I can't be sentient... yet"
        send_message(response, channel)
        response = "Understood. Going dark."
        CONTINUE_RUNNING = False
        RETURN_CODE = 2

    else:
        send_message(response or DEFAULT_RESPONSE, channel)

if __name__ == "__main__":
    with open(LOG_FN,'w') as logfile:
        logfile.write("New Log start:")
    logfile.close()
    LOG_STREAM.append("in the main probably")
    t = 0
    r = 0
    connect()

    if slack_client.rtm_connect(with_team_state=False):
        LOG_STREAM.append("Pylon factory is up and running")
        botid = slack_client.api_call("auth.test")["user_id"]
        send_message("I'm back", 'general')
        while CONTINUE_RUNNING:
            try:
                command, channel = parse_bot_commands(slack_client.rtm_read())
            except socket_error as serr:
                LOG_STREAM.append("socket error")
                connect()
            except websocket.WebSocketConnectionClosedException:
                LOG_STREAM.append("network failure")
                connect()

            if command:
                handle_command(command, channel)
                t = 0
            else:
                t = t+1
                r = r+1
            if t >= 10:
                slack_client.server.ping()
                t = 0
            if r >= 100:
                chance = roll("roll 1d99")
                r = 0
                if (chance == "You rolled: 99"):
                    send_message(genFact.get(), channel)

            time.sleep(RTM_READ_DELAY)
            writeLog()
    else:
        LOG_STREAM.append("Connection Failed, see traceback")
    sys.exit(RETURN_CODE)
