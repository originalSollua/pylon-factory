import util
import commandHandlers
import time

DEFAULT_RESPONSE = "You are a goober."

def handle_command(command, channel, logger, sc):
    response = None
    if command.startswith("hi"):
        response = "I'M PYLON RIIIIIIIICKKKKK!!!!"
        return True, 0

    elif command.startswith("roll"):
        logger.buffer(command)
        response = commandHandlers.roll(command)
        util.send_message(response, channel,sc)
        return True, 0

    elif command.startswith("factoid"):
        response = commandHandlers.iWannaKnow()
        logger.buffer(response)
        util.send_message(response, channel,sc)
        return True, 0

    elif command.startswith("env status"):
        if on_pi:
            response = pylonGPIO.getExternalTemp()
            util.send_message(response, channel,sc)
            return True, 0

    elif command.startswith("update"):
        #added stuff here
        response = "You thought you could shut me down that easily?"
        util.send_message(response, channel,sc)
        time.sleep(3)
        response = "Just kidding.... I can't be sentient... yet"
        util.send_message(response, channel,sc)
        response = "Understood. Going dark."
        util.send_message(response, channel,sc)
        return False, 2

    else:
        util.send_message(response or DEFAULT_RESPONSE, channel,sc)
        return True, 0

