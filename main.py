import os
import sys
import time
import errno
from socket import error as socket_error
from slackclient import SlackClient
import websocket
import util
from pylon_factory import PylonFactory

def main():
    global logger
    logger = util.Logger()
    logger.write("New Log start:")
    pylon_factory = botSetup()
    global t,r
    t = 0
    r = 0

    RTM_READ_DELAY = 1
    CONTINUE_RUNNING = True
    RETURN_CODE = 0

    while CONTINUE_RUNNING:
        try:
            event_list = slack_client.rtm_read()
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

        # Made the tick count always increase like a real one
        # Can be changed if need be
        t += 1
        r += 1
        RETURN_CODE = checkValue(pylon_factory.process(event_list, t, r))
        if RETURN_CODE:
            CONTINUE_RUNNING = False
        time.sleep(RTM_READ_DELAY)
        logger.write()

    sys.exit(RETURN_CODE)

# This is gross but I needed some way to reset the ticks when I don't have pointers
# Could increment the tick on a modulo and have actions be in a range instead
def checkValue(val):
    # pylon_factory.process() return values:
    # 00 - Message went through, or no independent action
    # 02 - Update message
    # 01 - t event, clear t
    # 10 - r event, clear r
    # 11 - both t and r event, clear both
    if val == 0 or val == 2:
        return val
    elif val == 1:
        t = 0
        return 0
    elif val == 10:
        r = 0
        return 0
    else:
        t = 0
        r = 0
        return 0

def botSetup():
    with open('.env','r') as env_file:
        bot_token = env_file.readline().rstrip().split("=")[1]
    logger.buffer(bot_token)
    global slack_client
    slack_client = connect(bot_token)
    if slack_client.rtm_connect(with_team_state=False):
        logger.buffer("Pylon factory is up and running")
        botid = slack_client.api_call("auth.test")["user_id"]
    else:
        logger.buffer("Connection Failed, see traceback")
        # May need to define RC for this
        sys.exit(1)
    return PylonFactory(slack_client, botid, logger)

def connect(token):
    logger.buffer("attempting connect")
    return SlackClient(token)

if __name__ == "__main__":
    main()
