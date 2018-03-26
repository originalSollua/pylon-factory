import random
import genFact

DIE_RANGE = range(1,100)

def roll(message_text, logger):
    num_dice = 0
    dice_size = 0
    dice_array = []
    logger.buffer(message_text)
    roll_com = message_text.split(" ")
    if roll_com[0] != "roll":
        return "I dont even know what happened"
    roll_nums  = roll_com[1].split("d")

    # Check if the values are integers
    try:
        num_dice  = int(roll_nums[0])
        dice_size = int(roll_nums[1])
    except ValueError:
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

def iWannaKnow(logger):
    tfact = genFact.get()
    logger.buffer(tfact)
    return tfact

