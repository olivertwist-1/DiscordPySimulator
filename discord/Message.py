from typing import Optional, Tuple, List, Union, Iterable, Generator
import random
from discord.embed import Embed


class Channel:
    all_messages: List[str] = []

    def __init__(self, msg: "Message") -> None:
        self.id = int(f"77{random.getrandbits(48)}")
        self.msg = msg

    async def send(self, msg: str = '', *, embed: Optional[Embed] = None) -> Union[str, Embed]:

        """
        To Simulate you are sending something in a channel

        Arguments:
            msg (str): The message to display
            embed (Optional[Embed]): The embed you are going to send. It's Optional

        Return:
            str = the message

        """
        id_ = self.id
        # this line is unneeded, i just added it because pycharm would not take this function as instantiated
        if not isinstance(msg, str):
            raise ValueError('only strings in send()')

        if embed is None:
            print(msg)
            return msg

        print(f"{msg}\n{embed.embedSender()}".strip())
        return embed

    async def history(self, *,
                      limit: Optional[int] = None
                      ) -> Generator[str, None, None]:

        """
        it will return a generator with the messages

        Arguments:
            limit (Optional[int]): the limit of messages you want to receive, use None if you expect all

        Return:
            Generator[str, None, None]: yield
        """
        times: int = 0

        all_messages = iter(self.all_messages)

        limit = limit if limit is not None else len(self.all_messages)

        while times < limit:
            try:
                yield next(all_messages)
            except StopIteration:
                break
            times += 1




class Message:

    def __init__(self):
        self.channel = Channel(self)
        self.__msg = None

    def new_message(self) -> None:
        Channel.all_messages.append(self.__msg)

    def set_message(self, new_msg: str) -> "Message":
        self.__msg = new_msg
        return self

    @property
    def content(self) -> str:
        return self.__msg

