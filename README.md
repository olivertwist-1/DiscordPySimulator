# DiscordPySimulator
It's a discord.py simulator.

## :warning: Things to fix

### Context
As you may know, discord py commands provide the context as the first parameter
(when not using classes) however my code doesn't have ctx as paramater, so to print use print() function.
The idea here is to do

```py
await ctx.send()
``` 
Just to settle for the original syntax.

### Infinite parameters
In discord.py when we want to receive several arguments and those are stored in one variable, we use unpack operator, look at the following example

```py
@bot.command()
async def example(ctx, first, *, second):
   pass
```

All arguments after * will be stored in `second`
So my bot doesn't provide this yet

### on_message
* __Needs to be below commands__
* __Needs to be used to start using commands through console__

## :wrench: Contribution
Feel free to contribute at this crazy repository. Add things related to it or fix things mentioned above

## How to use ❓
example

```py
import discord
import asyncio
from discord import *


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
# You may set help_command=None, but this simulator already provides a command display. Up to you
# prefix is mandatory to pass 


@bot.event
async def on_ready():
    print("hello")


@bot.command()
async def add(n1: int, n2: int):
    print(n1 + n2)

@bot.event
async def on_message(message: str):
    if message.startswith("hello"):
        print("Hello!")
        
    await bot.process_commands(message) # This needs to be used, mandatory


bot.run('token') # it doesn't need to be a real token.
```
### Helpers
```
1. Tekgar#0000
2. Nium#0000
```
Not allowed to expose their tag
