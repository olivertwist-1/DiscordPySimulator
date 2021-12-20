from inspect import isfunction


class UnknownEvent(Exception):
    def __init__(self, event: object):
        self.event = event

    def __str__(self):
        return f"{self.event} is not a valid event"


class ExistingFunction(Exception):
    def __init__(self, function):
        self.function = function.__name__ if isfunction(function) else function

    def __str__(self):
        return f"{self.function} already exists"


class UserIsSelfBot(Exception):

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class BotNotRan(Exception):
    def __init__(self, bot):
        self.bot = bot

    def __str__(self):
        return f"{self.bot.__class__.__name__}.run(TOKEN) has to be done"


class NoArgumentsInOnReady(Exception):
    def __str__(self):
        return f"No arguments in on_ready"



class NonCoroutineFunction(Exception):
    def __init__(self, func):
        self.func = func

    def __str__(self):
        return f"{self.func.__name__} has to be a coroutine"


class NoArgumentsInOnMessage(Exception):
    def __str__(self):
        return f"on_message() needs message as parameter"


class ExceededArgumentsOnMessage(Exception):
    def __str__(self):
        return f"on_message() receives only 1 parameter"


class CommandNotFound(Exception):
    def __init__(self, command: str):
        self.command = command

    def __str__(self):
        return f"Command {self.command} was not found"
