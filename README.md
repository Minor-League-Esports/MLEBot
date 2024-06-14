# MLE Bot

MLE Bot is a Minor League E-Sports Franchise ready, python written Discord Bot.

## :bulb: Features :bulb:
- .env file for control over environments of your Franchise
- sprocket connectivity to get latest public dataset data
- roster channel support to automatically show your team off!
- sprocket player lookup for easy player tracking/management
- team-eligibility commands to stay on top of non-eligible players!
- season stats to get pretty html/css images!

## :dependabot: Setup :dependabot:
:warning: **Attention:** At this very moment, this setup is meant to run locally on a machine. This will run in a command console.
If you close the console, the bot goes down. :warning:

You can find an example in the following github repo!
- https://github.com/iroxusux/DemoMLEBot

Start off by creating a new project and adding both this repository and PyDiscoBot to your project either directly or via PyPi! Super Easy!
``` python
python -m pip install MLEBot
python -m pip install PyDiscoBot
```

### :memo: Fill out the .env file to customize your bot! :memo:


Make sure to include these imports!
```python
import discord
from discord.ext import commands
import dotenv
import os
import PyDiscoBot
from MLEBot import mle_commands, mle_bot
```

Create a custom class for your bot!
```python
class MyBot(mle_bot.MLEBot):
    def __init__(self,
                 command_prefix: str | None = None,
                 bot_intents: discord.Intents | None = None,
                 command_cogs: [discord.ext.commands.Cog] = None):
        super().__init__(command_prefix=command_prefix,
                         bot_intents=bot_intents,
                         command_cogs=command_cogs)
```

To add functionality when the bot comes online, over-ride the on-ready function of the bot!
```python
async def on_ready(self,
                       suppress_task=False) -> None:
        await super().on_ready(suppress_task)  # remember to call the parent class here!
        # do_some_code_here!!!
```

To add functionality to each of the bot's "ticks", over-ride the on_task function of the bot!
```python
    async def on_task(self) -> None:
        await super().on_task()  # remember to call the parent class here!
        # do some task-y stuff here!
```

Run your file!
```python
if __name__ == '__main__':
    dotenv.load_dotenv()

    intents = discord.Intents(8)
    # noinspection PyDunderSlots
    intents.guilds = True
    # noinspection PyDunderSlots
    intents.members = True
    # noinspection PyDunderSlots
    intents.message_content = True
    # noinspection PyDunderSlots
    intents.messages = True
    # noinspection PyDunderSlots
    intents.reactions = True

    bot = MyBot('ub.',
                intents,
                [PyDiscoBot.Commands,
                 mle_commands.MLECommands])

    bot.run(os.getenv('DISCORD_TOKEN'))
```

## :computer: Development Status :computer:

Build - :construction: beta

Version - 1.0.4

### Requirements
PyDiscoBot==1.0.4
  - https://github.com/iroxusux/PyDiscoBot

## :soccer: Join MLE Today! :soccer:
:sparkler: Main Site:
  - https://mlesports.gg/
    
:postbox: Apply Today!:
  - https://mlesports.gg/apply
    
:camera: Check out our twitter!:
  - https://twitter.com/mlesportsgg
