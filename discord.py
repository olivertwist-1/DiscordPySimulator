import functools
from functools import wraps
from collections import Iterable
import sys
import dis
from typing import Union, Optional
import inspect
from CustomExceptions import *
import atexit
import sys
import asyncio
import shlex


class Intents:

    @classmethod
    def all(cls):
        return

    @classmethod
    def default(cls):
        return



class Events:
    possible_events = ['on_message',
                       'on_ready']


def check_called(f) -> object:
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return f(*args, **kwargs)

    wrapper.call_count = 0
    return wrapper


class commands:
    class Bot:
        bot_ran: bool = False

        def __init__(self, command_prefix: str, *,
                     intents=None,
                     help_command: Optional[bool] = True) -> object:

            self.command_used = 0
            self.prefix = command_prefix
            self.intents = intents
            self.help_command = help_command
            self.bot_commands: dict = {}
            self.command_used: int = 0
            self.occurred_exceptions: int = 0
            self.on_message_used: int = 0
            atexit.register(self.bot_run_called)

        def command(self, aliases=None):
            if aliases is None:
                aliases = []
            aliases = [1] if not aliases else aliases

            def wrapper(function):

                if not inspect.iscoroutinefunction(function):
                    raise NonCoroutineFunction(function)

                if function.__name__ == "help" or "help" in aliases:

                    if self.help_command is not None:
                        # self.occurred_exceptions += 1
                        raise ExistingFunction('help')

                for al in aliases:
                    for main_func in self.bot_commands:
                        if function.__name__ == main_func.__name__ or \
                                function.__name__ in self.bot_commands[main_func]:

                            raise ExistingFunction(function)

                        if isinstance(al, str):
                            if al == main_func.__name__ or \
                                    al in self.bot_commands[main_func]:

                                raise ExistingFunction(al)

                self.bot_commands[function] = [f for f in aliases]

                @wraps(function)
                async def parameters(*args, **kwargs):

                    print("Running command: ", end='')

                    if commands.Bot.arguments_length(function) > 0:
                        await function(*args, **kwargs)
                    else:
                        await function()

                return parameters

            return wrapper

        @staticmethod
        def get_func(func: callable) -> inspect:
            """Returns the command INFO
                 EXAMPLE: type_hints, variables, its values
            """
            return inspect.getfullargspec(func)

        @staticmethod
        def arguments_length(func):
            """returns the amount of arguments the given function has"""
            return len(inspect.getfullargspec(func).args)

        def aliases(self, function) -> list:
            """returns all aliases of a certain function"""
            return list(filter(lambda x: isinstance(x, str), self.bot_commands.get(function.__name__)))

        @property
        def commands(self):
            """returns all commands from the bot instance"""
            return list(self.bot_commands.keys())

        @check_called
        def run(self, token: str, *, bot=True) -> None:
            """'Runs' the bot instance"""
            if not bot:
                raise UserIsSelfBot('Oliver\'s library doesn\'t allow selfbots')

            self.command_used += 1

            if self.command_used > 1:
                raise Exception('You can\'t run twice')

        def bot_run_called(self):
            if not self.run.call_count:
                if not getattr(sys, "last_traceback", None):
                    raise BotNotRan(self)

        class event:
            def __init__(self, function: callable):
                self.function = function

                if self.function.__name__ not in Events.possible_events:
                    raise UnknownEvent(self.function)

                if not inspect.iscoroutinefunction(self.function):
                    raise NonCoroutineFunction(self.function)

                asyncio.run(self.__call__())


            async def __call__(self):
                if self.function.__name__ == "on_ready":
                    if not commands.Bot.arguments_length(self.function):
                        if not getattr(sys, "last_traceback", None):
                            await self.function()
                    else:
                        raise NoArgumentsInOnReady


                elif self.function.__name__ == "on_message":

                    amount_arguments = commands.Bot.arguments_length(self.function)

                    if not amount_arguments:
                        raise NoArgumentsInOnMessage

                    elif amount_arguments > 1:
                        raise ExceededArgumentsOnMessage
                    else:
                        while True:
                            message_user = input('COMMAND: ')
                            await self.function(message_user)


        async def process_commands(self, message: str) -> None:
            if message.startswith(self.prefix):
                func_call = message.split()



                command_name = func_call[0][len(self.prefix):]

                ignore_raise: bool = False
                if command_name == "help" and self.help_command:
                    ignore_raise = True
                    display: list = []
                    for func in self.bot_commands:
                        display.append(f"   {func.__name__}\n    - {func.__doc__}")
                    print('\n\n'.join(display))


                for func_command in self.bot_commands:
                    if command_name == func_command.__name__ or \
                            command_name in self.bot_commands[func_command]:

                        parameters = shlex.split(' '.join(func_call[1:]))

                        type_hints = []
                        for v in commands.Bot.get_func(func_command).args:
                            type_hints.append((v, 0))
                            # fills the second value of tuple, so it can be refilled with a type

                        for index, (var, typ) in enumerate(type_hints):
                            cmd_info = commands.Bot.get_func(func_command)

                            type_hints[index] = (var, cmd_info.annotations[var] if var in cmd_info.annotations else str)

                        zipped = list(zip(parameters, type_hints))

                        new_arguments = []

                        for variable, (var, type_) in zipped:
                            new_arguments.append(type_(variable))

                        return await func_command(*new_arguments)
                else:
                    if not ignore_raise:
                        raise CommandNotFound(command_name)


