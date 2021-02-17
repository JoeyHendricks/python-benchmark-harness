from QuickPotato.profiling.intrusive import performance_critical
import time
import math


@performance_critical
def slow_method():
    num = 6 ** 6 ** 6
    return len(str(num))


@performance_critical
def fast_method():
    num = 6 ** 6 ** 6
    return int(math.log10(num))


class FancyCode:
    """
    A totally random piece of code used to example quick profiling.
    """

    @performance_critical
    def say_my_name_and_more(self, name):
        print(f"Your name is: {self.capitalize_name(name)}\n")
        print(f"The length of your name is: {self.length_of_name(name)}")
        print(f"Your name in lowercase: {self.lowercase_name(name)}")
        print(f"Your name in uppercase: {self.uppercase_name(name)}")
        self.sleep_based_on_name_length(name)

    @staticmethod
    def capitalize_name(name):
        """
        Your name but capitalized
        :param name: your name
        :return: Your name but capitalized
        """
        return name.capitalize()

    def length_of_name(self, name):
        """
        Will count the length of your name
        :param name: your name
        :return: The length of your name
        """
        length = len(name)
        if length > 10:
            self.show_message_when_name_very_long()
        return length

    def show_message_when_name_very_long(self):
        print("You have a long name ;)")
        self.x()

    def x(self):
        self.y()
        return True

    def y(self):
        self.foo()
        print("deep")
        return True

    @staticmethod
    def foo():
        return True

    def sleep_based_on_name_length(self, name):
        """
        Will sleep based on the length of your  name.
        :param name: Your  name
        :return: True because you waited :)
        """
        length = int(self.length_of_name(name))
        time.sleep(length)
        return True

    @staticmethod
    def uppercase_name(name):
        """
        Converts your name to all CAPS!
        :param name: Your name
        :return: Will return you name in all CAPS
        """
        return name.upper()

    @staticmethod
    def lowercase_name(name):
        """
        Converts your name to all lower case.
        :param name: Your name
        :return: Will return you name in all lowercase
        """
        return name.lower()
