import commandHandlers
GPIO_on = True
try:
    import pylonGPIO
except ImportError as importError:
    GPIO_on = False

DEFAULT_RESPONSE = "You are a goober."

def handle_command(command, channel):
    response = None
    rc = 0
    if command.startswith("hi"):
        response = "I'M PYLON RIIIIIIIICKKKKK!!!!"

    elif command.startswith("roll"):
        response = commandHandlers.roll(command)

    elif command.startswith("factoid"):
        response = commandHandlers.iWannaKnow()

    elif command.startswith("env status"):
        if GPIO_on:
            response = pylonGPIO.getExternalTemp()

    elif command.startswith("update"):
        response = "Understood. Going dark."
        rc = 2

    else:
        response = DEFAULT_RESPONSE

    return response, rc
