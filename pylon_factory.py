import os
import sys
import time
import re
import errno
from socket import error as socket_error
from slackclient import SlackClient
import websocket
import util
import commandHandlers
import eventHandlers

on_pi = True
try:
    import pylonGPIO
except ImportError as importError:
    on_pi = False
    print(importError)

#activate a slackbot instance
#slackbot userid
botid = None

#constants
RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
CONTINUE_RUNNING = True
RETURN_CODE = 0
CON_T = 0
SHRUG_MAN = "¯\_(ツ)_/¯"
if on_pi:
    pylonGPIO.initPylonIO()

def connect():
    logger.buffer("attempting connect")
    global slack_client
    slack_client = SlackClient(bot_token)

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_dm(event["text"], event["channel"])
            if user_id == botid:
                logger.buffer(message)
                return message, event["channel"]
    return None, None

def parse_dm(message_text, channel):
    logger.buffer(message_text)
    if on_pi:
        pylonGPIO.lcdLog(message_text)
    global CON_T
    CON_T = CON_T+1
    if CON_T >= 10:
        util.send_message(commandHandlers.iWannaKnow(logger),"general",slack_client)
        CON_T = 0
    if SHRUG_MAN in message_text:
        util.send_message(SHRUG_MAN, channel,slack_client)
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

if __name__ == "__main__":
    logger = util.Logger()
    logger.write("New Log start:")
    logger.buffer("in the main probably")
    t = 0
    r = 0
    global bot_token
    with open('.env','r') as env_file:
        bot_token = env_file.readline().rstrip().split("=")[1]
    logger.buffer(bot_token)
    connect()

    if slack_client.rtm_connect(with_team_state=False):
        logger.buffer("Pylon factory is up and running")
        botid = slack_client.api_call("auth.test")["user_id"]
        util.send_message("I'm back", 'general',slack_client)
        while CONTINUE_RUNNING:
            try:
                command, channel = parse_bot_commands(slack_client.rtm_read())
            except socket_error as serr:
                logger.buffer("socket error")
                connect()
            except websocket.WebSocketConnectionClosedException:
                logger.buffer("network failure")
                connect()
            except AttributeError:
                logger.buffer("Numpy again")
                pass
            #    connect()

            if command:
                CONTINUE_RUNNING, RETURN_CODE = eventHandlers.handle_command(command, channel,logger, slack_client)
                t = 0
            else:
                t = t+1
                r = r+1
                if on_pi:
                    pylonGPIO.lcdTick()
            if t >= 10:
                try:
                    slack_client.server.ping()
                except:
                    logger.buffer("Why would ping fail?")
                t = 0
                if on_pi:
                    temp = pylonGPIO.readCoreTemp()
                    if int(temp) >= 48000:
                        util.send_message('*WARNING THERMAL OVERLOAD IN PROGRESS!*',
                                'bot_spam',slack_client)
                        util.send_message('CORE TEMPERATURE IS: '+str(temp),
                                'bot_spam',slack_client)
                        if not pylonGPIO.fanOn:
                            pylonGPIO.activateFan()
                    elif int(temp) < 45000 and pylonGPIO.fanOn:
                        util.send_message('Thermal crisis averted.',
                                'bot_spam',slack_client)
                        pylonGPIO.deactivateFan()
                    else:
                        logger.buffer('nothing to report')
                else:
                    logger.buffer('GPIO library not imported: no temp data')

            if r >= 100:
                chance = commandHandlers.roll("roll 1d99")
                r = 0
                if (chance == "You rolled: 99"):
                    util.send_message(commandHandlers.iWannaKnow(logger),
                            channel,slack_client)

            time.sleep(RTM_READ_DELAY)
            logger.write()
    else:
        logger.buffer("Connection Failed, see traceback")
    sys.exit(RETURN_CODE)
