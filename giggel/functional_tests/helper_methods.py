import string
import random


class helperMethods():

        # helper method - random string generator
    def generate_string(length):
        randString = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=length))
        return randString
