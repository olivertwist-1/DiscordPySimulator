# DiscordPySimulator
It's a discord.py simulator.

## :warning: Things to fix

### Infinite parameters
In discord.py when we want to receive several arguments and those are stored in one variable, we use unpack operator, look at the following example

```py
@bot.command()
async def example(ctx, first, *, second):
   pass
```

All arguments after * will be stored in `second`
So my console bot doesn't provide this yet

### Variables Initialized on Parameters
This needs to be added in `process_commands` function from bot class.

```py
@bot.command()
async def add(ctx, n1: int, n2: int = 2):
    await ctx.send(str(n1 + n2))
```
When you call this function (command), you will only need to pass 1 argument, since n2 was assigned some value. 
My console bot can't do this yet

### on_message
* __Needs to be below commands, ALL__

## :wrench: Contribution
Feel free to contribute at this crazy repository. Add things related to it or fix things mentioned above

## How to use ❓
example

```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", help_command=True, intents=discord.Intents.all())


@bot.command(aliases=["addition"])
async def add(ctx: commands.Context, n1: int, n2: int):
    await ctx.send(f"Result: {n1+n2}")


@bot.command(aliases=["multiplication"])
async def mul(ctx: commands.Context, n1: int, n2: int):
    await ctx.send(f"Result: {n1 * n2}")


@bot.command()
async def rules(ctx: commands.Context):
    embed = discord.Embed(title="Rules of the server",
                          description="1. First rule\n2. Second rule\n3. Third rule\n4. Fourth rule",
                          color=discord.Colour.blue())

    await ctx.send(embed=embed)


@bot.command()
async def get_messages(ctx: commands.Context, limit: int):
    messages = []

    async for message in ctx.channel_history(limit=limit):
        messages.append(message)

    for index, msg in enumerate(messages):
        await ctx.send(msg)



@bot.event
async def on_ready():
    print("bot is ready")


@bot.event
async def on_message(msg: discord.Message):
    if msg.content.startswith("hello"):
        await msg.channel.send("hello, let me send an embed! use 'show_embed'")

    if msg.content.startswith("show_embed"):
        embed = discord.Embed(title="hello",
                              description="Here goes the description",
                              footer="the footer",
                              color=discord.Colour.yellow())
        await msg.channel.send(embed=embed)

    if msg.content.startswith("messages"):
        async for message in msg.channel.history(limit=5):
            await msg.channel.send(message)

    await bot.process_commands(msg.content)

bot.run("token")
```

### Ideas ❗
__Adding Cogs__
`only this for now`

### Helpers
```
1. Tekgar#0000
2. Nium#0000
```
Not allowed to expose their tag
