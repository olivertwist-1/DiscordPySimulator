from typing import List, Optional, Union, Dict


class Colour:
    _pink = '\033[95m'
    _blue = '\033[94m'
    _cyan = '\033[96m'
    _green = '\033[92m'
    _yellow = '\033[93m'
    _red = '\033[91m'
    reset = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

    pink_bold = _pink + bold
    blue_bold = _blue + bold
    cyan_bold = _cyan + bold
    green_bold = _green + bold
    yellow_bold = _yellow + bold
    red_bold = _red + bold

    @classmethod
    def pink(cls):
        return cls._pink

    @classmethod
    def yellow(cls):
        return cls._yellow

    @classmethod
    def blue(cls):
        return cls._blue

    @classmethod
    def cyan(cls):
        return cls._cyan

    @classmethod
    def green(cls):
        return cls._green

    @classmethod
    def red(cls):
        return cls._red


class Embed:
    def __init__(self, *,
                 title: Optional[str] = None,
                 description: Optional[str] = None,
                 color: Optional[str] = None,
                 footer: Optional[str] = None) -> None:

        self._title = title
        self._description = description
        self._color = color
        self._footer = footer

    def __repr__(self) -> str:
        return f"<Embed title='{self._title}'" \
               f" description='{self._description}'" \
               f" footer='{self._footer}'>"

    def set_title(self, new_title: str) -> "Embed":
        self._title = new_title
        return self

    def set_description(self, new_description: str) -> "Embed":
        self._description = new_description
        return self

    def set_color(self, new_color: str) -> "Embed":
        self._color = new_color
        return self

    def set_footer(self, new_footer: str) -> "Embed":
        self._footer = new_footer
        return self


    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def footer(self) -> str:
        return self._footer

    @property
    def color(self) -> str:
        return self._color

    @staticmethod
    def add_lines(text: str) -> str:
        new_ = []

        for line in text.splitlines():
            # if not line.startswith('|')
            #   new_.append(f"| {line}")
            # else:
            #   new_.append(line)
            new_.append(f"{'|' if not line.startswith('|') else ''} {line}")

        return "\n".join(new_).strip()

    def embedSender(self) -> str:

        """
        Sends an "embed"

        Example:
            embed = discord.Embed(title="My Title", description="The description", footer="The footer")
             -> | My Title
                |
                | The description
                |
                | The footer

        Return:
            str = the format of embed
        """

        items_ignore = {}
        embed_dict = {"title": None, "description": None, "footer": None, "color": None}

        color = self.color if self.color is not None else Colour.reset
        # color will be empty if color from embed instance is None

        title = self.title
        description = self.description
        footer = self.footer


        if title is not None:
            embed_dict["title"] = f"{Colour.bold}{title}{Colour.reset}"

        if description is not None:
            embed_dict["description"] = description

        if footer is not None:
            embed_dict["footer"] = footer

        if color is not None:
            embed_dict["color"] = color

        format_ = []

        if embed_dict["title"] is not None:
            format_.append(Embed.add_lines(f"| {embed_dict['title']}"))

        if embed_dict["description"] is not None:
            format_.append("| ")
            format_.append(Embed.add_lines(f"| {embed_dict['description']}").strip())

        if embed_dict["footer"] is not None:
            format_.append("| ")
            format_.append(Embed.add_lines(f"| {embed_dict['footer']}".strip()))

        format_ = "\n".join(format_).splitlines()

        for index, line in enumerate(format_):
            format_[index] = format_[index].replace("|", f"{color}|{Colour.reset}", 1)

        return "\n".join(format_)




