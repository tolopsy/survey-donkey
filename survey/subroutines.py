import string
import random


# to generate eight value id
def random_id(character=8):
    letters = string.ascii_letters + string.digits
    choice_letter = ''.join(random.choice(letters) for _ in range(character))
    return choice_letter
