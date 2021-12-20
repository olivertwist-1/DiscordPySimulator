# DiscordPySimulator
It's a discord.py simulator.

## :warning: Things to fix

### Context
As you may know, discord py commands provide the context as the first parameter (when not using classes) however my code doesn't have ctx as paramater, so to print use print() function.

### Infinite parameters
In discord.py when we want to receives several arguments and those are stored in one variable, we use unpack operator, look at the following example

```py
@bot.command()
async def example(ctx, first, *, second):
   pass```

All arguments after * will be stored in `second`
So my bot doesn't provide this yet

### on_message

