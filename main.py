import discord, board, os, json
from discord import app_commands
from typing import Optional

CONFIG_PATH = os.path.join("config","settings.dat")

def config():
    if not os.path.exists(os.path.dirname(CONFIG_PATH)):
        os.makedirs(os.path.dirname(CONFIG_PATH))

    if not os.path.exists(CONFIG_PATH):
        #generate default config
        config_dic = {
                "token" : "",
                "owners" : [
                    0000
                    ],
                "command_servers" : [
                    0000
                    ]
            }
        with open(CONFIG_PATH, "w") as config_file:
            json.dump(config_dic, config_file, indent=4)
            print("please fill in bot token and any bot admin discord ids to the new config.json file!")
            quit()
    else:
        with open(CONFIG_PATH) as config_file:
            return json.load(config_file)

class newClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        

    async def setup_hook(self):
        for guild_id in config()["command_servers"]:
            try:
                guild = discord.Object(id=guild_id)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
            except:
                pass
        await self.tree.sync()

client = newClient(intents = discord.Intents.default())

@client.event
async def on_ready():
    print(f"logged in as {client.user} with token {config()['token']} to {len(client.guilds)} servers")

@client.tree.error
async def on_app_command_error(interaction, error):
    await interaction.response.send_message(f"The following error was encountered: {str(error.__cause__)}. Let Abyss know!", ephemeral=True)

def prog_options():
    opt = ["Act 1 Only", "No Clawline", "No Feydown"]
    return [app_commands.Choice(name=i, value=i) for i in opt]

@client.tree.command()
@app_commands.describe(progression="Limit the highest progression needed for any goal.")
@app_commands.choices(progression=prog_options())
async def newboard(interaction: discord.Interaction, progression: Optional[app_commands.Choice[str]] = None):
    """Generates a new board for bingosync."""
    if progression == "Act 1 Only":
        noTags = ["act2", "clawline", "feydown"]
    elif progression == "No Clawline":
        noTags = ["clawline", "feydown"]
    elif progression == "No Feydown":
        noTags = ["feydown"]
    else:
        noTags = []
    thisBoard = board.bingosyncBoard(noTags=noTags)
    await interaction.response.send_message(json.dumps(thisBoard), ephemeral=True)

if __name__ == "__main__":
    client.run(config()["token"])