import os
import sys
import time
import re
import errno
import random
from socket import error as socket_error
from slackclient import SlackClient
import websocket


#activate a slackbot instance
print("first point")
global bot_token
with open('.env','r') as env_file:
    bot_token = env_file.readline().rstrip().split("=")[1]
print("token=" + bot_token)
print("after gettoken")
#slackbot userid
botid = None

#constants
RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
CONTINUE_RUNNING = True
RETURN_CODE = 0

def roll(message_text):
    #stub
    num_dice = 0
    dice_size = 0
    dice_array = []
    print(message_text)
    roll_com = message_text.split(" ")
    print(roll_com)
    if roll_com[0] != "roll":
        return "I dont even know what happened"
    roll_nums  = roll_com[1].split("d")
    
    if (int(roll_nums[0]) >= 1 and int(roll_nums[0]) <= 99):
        num_dice = int(roll_nums[0])
    if (int(roll_nums[1]) >= 1 and int(roll_nums[1]) <= 99):
        dice_size = int(roll_nums[1])
    if (num_dice == 0 or dice_size == 0):
        return "Invaild roll parameters. Please use (1-99)d(1-99)"
    for x in range(num_dice):
        dice_array.append(random.randint(1,dice_size))
    output = ""
    for x in range(len(dice_array)-2):
        output += str(x) +", "
    output += str(dice_array[len(dice_array)-1])
    return "You rolled: "+output

def get_random_fact():
    fact = "Did you know that: the Sun is a deadly laser"
    return fact

def connect():
    print("attempting connect")
    global slack_client
    slack_client = SlackClient(bot_token)

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_dm(event["text"])
            if user_id == botid:
                print(message)
                return message, event["channel"]
    return None, None

def parse_dm(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def send_message(message, channel):
    default = ""
    slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text = default or message
            )
    return

def handle_command(command, channel):
    default_response = "You are a goober."
    response = None
    if command.startswith("hi"):
        response = "I'M PYLON RIIIIIIIICKKKKK!!!!"

    if command.startswith("roll"):
        response = roll(command)
        slack_client.api_call(
                "chat.postMessage",
                channel=channel,
                text=response or default_response
                )

    if command.startswith("update"):
        global CONTINUE_RUNNING
        global RETURN_CODE
        #added stuff here
        response = "You thought you could shut me down that easily?"
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )
        time.sleep(3)
        response = "Just kidding.... I can't be sentient... yet"
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )
        response = "Understood. Going dark."
        CONTINUE_RUNNING = False
        RETURN_CODE = 1

    else: 
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
    )

if __name__ == "__main__":
    print("in the main probably")
    t = 0
    r = 0
    connect()

    if slack_client.rtm_connect(with_team_state=False):
        print("Pylon factory is up and running")
        botid = slack_client.api_call("auth.test")["user_id"]
        slack_client.api_call(
                "chat.postMessage",
                channel='general',
                text="I'm back"
        )
        while CONTINUE_RUNNING:
            try:
                command, channel = parse_bot_commands(slack_client.rtm_read())
            except socket_error as serr:
                print ("socket error")
                connect()
            except websocket.WebSocketConnectionClosedException:
                print ("network failure")
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
                    send_message(get_random_fact(), channel)

            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection Failed, see traceback")
    sys.exit(RETURN_CODE)
