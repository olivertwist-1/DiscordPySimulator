from inspect import isfunction


class UnknownEvent(Exception):
    """When event is not valid"""
    def __init__(self, event: callable):
        self.event = event

    def __str__(self):
        return f"{self.event.__name__} is not a valid event"


class ExistingFunction(Exception):
    """When this function already exists"""
    def __init__(self, function):
        self.function = function.__name__ if isfunction(function) else function

    def __str__(self):
        return f"{self.function} already exists"


class UserIsSelfBot(Exception):
    """When user sets to False in bot argument from run() function"""

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class BotNotRan(Exception):
    """when bot instance is not ran"""
    def __init__(self, bot):
        self.bot = bot

    def __str__(self):
        return f"{self.bot.__class__.__name__}.run(TOKEN) has to be done"


class NoArgumentsInOnReady(Exception):
    """when user pass arguments in on_ready"""
    def __str__(self):
        return f"No arguments in on_ready"



class NonCoroutineFunction(Exception):
    """When given function is not a Coroutine"""
    def __init__(self, func):
        self.func = func

    def __str__(self):
        return f"{self.func.__name__} has to be a coroutine"


class NoArgumentsInOnMessage(Exception):
    """When user pass No argument in on_message"""
    def __str__(self):
        return f"on_message needs message as parameter"


class ExceededArgumentsOnMessage(Exception):
    """When you pass more than 1 argument in on_message function"""
    def __str__(self):
        return f"on_message receives only 1 parameter"


class CommandNotFound(Exception):
    """When a command is not valid"""
    def __init__(self, command: str):
        self.command = command

    def __str__(self):
        return f"Command {self.command} was not found"


class ExceedCharactersTitle(Exception):
    """When many characters were used in title argument from Embed class"""

    def __init__(self, var):

        if isinstance(var, str):
            self.var = var
        else:
            raise ValueError(f'{var} has to be of type str, not {type(self.var)}')

    def __str__(self):
        return f"Limit of characters is 20"
