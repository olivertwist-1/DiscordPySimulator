from functools import wraps
from typing import Union, Optional, Dict, List, Callable, Coroutine, Any, Tuple, Generator
import inspect
from discord.ext.errors.CustomExceptions import *
import atexit
import sys
import asyncio
import shlex
from discord.Message import Message, Channel
from discord.embed import Embed
from discord.Intents import Intents


class Events:
    possible_events = ['on_message',
                       'on_ready']


def check_called(f) -> Callable[[Any], Coroutine]:
    def wrapper(*args, **kwargs) -> Coroutine:
        wrapper.call_count += 1
        return f(*args, **kwargs)

    wrapper.call_count = 0
    return wrapper


class Context:

    @staticmethod
    async def send(message: str = '', *,
                   embed: Optional[Embed] = None) -> Union[str, Embed]:
        """
        Arguments:
            message (str): The message to send
            embed (Optional[Embed]): the embed to send. It's Optional

        Return:
            str = The message
        """

        if not isinstance(message, str):
            raise ValueError('only strings')

        if embed is None:
            print(message)
            return message

        print(f"{message}\n{embed.embedSender()}".strip())
        return embed

    @classmethod
    async def channel_history(cls, *, limit: Optional[int] = None) -> Generator[str, None, None]:

        """
        it will return a generator with the messages

        Arguments:
            limit (Optional[int]): the limit of messages you want to receive, use None if you expect all


        Return:
            Generator[str, None, None]: yield
        """
        times: int = 0

        all_messages = iter(Channel.all_messages)

        limit = limit if limit is not None else len(Channel.all_messages)

        while times < limit:
            try:
                yield next(all_messages)
            except StopIteration:
                break
            times += 1


class Bot:
    bot_ran: bool = False

    def __init__(self, command_prefix: str, *,
                 intents: Intents = None, help_command: Optional[bool] = True) -> None:

        self.command_used = 0
        self.prefix = command_prefix
        self.intents = intents
        self.help_command: bool = help_command
        self.bot_commands: Dict[Callable, str] = {}
        self.command_used: int = 0
        self.occurred_exceptions: int = 0
        self.on_message_used: int = 0
        self.created_events: Dict[str, Callable] = {}
        atexit.register(self.__bot_run_called)

    @staticmethod
    def zip_args_annotations(args: List[str],
                             annotations: Dict[str, type]
                             ) -> List[Tuple[str, type]]:

        new_list: List[Tuple[str, type]] = []

        for var_name in args:
            if var_name in annotations:
                new_list.append((var_name, annotations.get(var_name)))

        return new_list

    def command(self, aliases=None):
        if aliases is None:
            aliases = []
        aliases = [1] if not aliases else aliases

        def wrapper(function):

            value = Bot.get_func(function)
            value2 = Bot.zip_args_annotations(value.args, value.annotations)

            if value2[0][1] != Context:
                raise ValueError(f'Var {value[0][0]} has to be of type Context')

            if value.varkw:
                raise ValueError(f"kwargs not allowed")

            if not inspect.iscoroutinefunction(function):
                raise NonCoroutineFunction(function)

            if function.__name__ == "help" or "help" in aliases:

                if self.help_command is not None:
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

                if Bot.arguments_length(function) > 0:
                    await function(Context, *args, **kwargs)
                else:
                    await function(Context)

            return parameters

        return wrapper

    @staticmethod
    def get_func(func: callable) -> inspect.FullArgSpec:
        """
        command info such as: hints, variables and its initialized values, and more

        Return:
            FullArgSpec = a class from inspect
        """
        return inspect.getfullargspec(func)

    @staticmethod
    def arguments_length(func: Callable) -> int:
        """
        returns the amount of arguments the given function has

        Arguments:
            func (Callable): the function

        Return:
            int = A number

        """
        return len(inspect.getfullargspec(func).args)

    def aliases(self, function: Callable) -> List[str]:
        """
        returns all aliases of a certain command (function)

        Arguments:
            function (Callable): the function

        Return:
            (List[str]) = A list with strings
        """
        return list(filter(lambda x: isinstance(x, str), self.bot_commands.get(function.__name__)))

    @property
    def commands(self):
        """returns all commands from the bot instance"""
        return list(self.bot_commands.keys())

    @check_called
    def run(self, token: str, *, bot=True) -> None:
        """
        'Runs' the bot instance

        Arguments:
            token (str): Does not need to be a real token, however,
            the more real it looks like, the better it will be to look like real one

            bot (bool): raises en Error if false since self bots not allowed, otherwise it runs fine

        Return:
            None = No value

        """
        if not bot:
            raise UserIsSelfBot('Oliver\'s library does not allow self bots')

        self.command_used += 1

        if self.command_used > 1:
            raise Exception('You can\'t run twice')

        asyncio.run(self.__run_all_events())

    async def __run_all_events(self):

        event_going: bool = True

        message_object = Message()
        # to receive the message through console

        func = self.created_events.get("on_message")

        while event_going:
            message_in = input("message: ")

            message_object.set_message(message_in)

            if message_in not in message_object.channel.all_messages:
                message_object.new_message()

            if func is not None:
                await func(message_object)
            else:
                await self.process_commands(message_in)

    def __bot_run_called(self) -> None:
        if not self.run.call_count:
            if not getattr(sys, "last_traceback", None):
                raise BotNotRan(self)

    def event(self, func: Callable[[Optional[str]], Any]) -> None:

        if func.__name__ not in Events.possible_events:
            raise UnknownEvent(func)

        if not inspect.iscoroutinefunction(func):
            raise NonCoroutineFunction(func)

        if func.__name__ == "on_ready":
            if not Bot.arguments_length(func):
                if not getattr(sys, "last_traceback", None):
                    asyncio.run(func())
            else:
                raise NoArgumentsInOnReady

        elif func.__name__ == "on_message":

            amount_arguments = Bot.arguments_length(func)

            if not amount_arguments:
                raise NoArgumentsInOnMessage

            elif amount_arguments > 1:
                raise ExceededArgumentsOnMessage

            self.created_events[func.__name__] = func

    async def process_commands(self, message: str) -> Optional[Coroutine]:

        if not isinstance(message, str):
            raise ValueError(f'Argument must be a string, not {type(message)}')

        if message.startswith(self.prefix):
            func_call = message.split()

            command_name = func_call[0][len(self.prefix):]

            ignore_raise: bool = False
            if command_name == "help" and self.help_command:
                ignore_raise = True
                display: List[str] = []
                for func in self.bot_commands:
                    display.append(f"   {func.__name__}\n    - {func.__doc__}")
                print('\n\n'.join(display))

            for func_command in self.bot_commands:
                if command_name == func_command.__name__ or \
                        command_name in self.bot_commands[func_command]:

                    parameters = shlex.split(' '.join(func_call[1:]))

                    type_hints = []
                    for v in Bot.get_func(func_command).args[1:]:
                        type_hints.append((v, 0))
                        # fills the second value of tuple, so it can be refilled with a type

                    for index, (var, typ) in enumerate(type_hints):
                        cmd_info = Bot.get_func(func_command)

                        type_hints[index] = (var, cmd_info.annotations[var] if var in cmd_info.annotations else str)

                    zipped = list(zip(parameters, type_hints))

                    new_arguments = []

                    for variable, (var, type_) in zipped:
                        new_arguments.append(type_(variable))

                    return await func_command(Context, *new_arguments)
            else:
                if not ignore_raise:
                    raise CommandNotFound(command_name)
