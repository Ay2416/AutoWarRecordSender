# Discord bot import
import discord
from discord.ext import commands
from discord import app_commands

# My program import
from Cogs.CommandPrograms.send_add import add
from Cogs.CommandPrograms.send_delete import delete
from Cogs.CommandPrograms.send_list import list

@app_commands.guild_only()
class send(app_commands.Group):
    def __init__(self, bot: commands.Bot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
    
    # /send *
    # /send add
    @app_commands.command(name="add",description="戦績を送信するプレイヤーを追加します。 / The War record send player add.")
    #@app_commands.describe(url="YouTubeチャンネルのURL")
    @app_commands.choices(normal_mention=[discord.app_commands.Choice(name="on",value="on"),discord.app_commands.Choice(name="off",value="off")])
    @app_commands.choices(rankup_notification=[discord.app_commands.Choice(name="on",value="on"),discord.app_commands.Choice(name="off",value="off")])
    @app_commands.choices(rankup_mention=[discord.app_commands.Choice(name="on",value="on"),discord.app_commands.Choice(name="off",value="off")])
    async def send_add(self, interaction: discord.Interaction,lounge_name:str,channel:discord.TextChannel,normal_mention:str,rankup_notification:str=None,rankup_mention:str=None):

        if rankup_notification == None:
            rankup_notification = "off"
        
        if rankup_mention == None:
            rankup_mention = "off"
        
        await add().add_info(interaction, lounge_name, channel, normal_mention, rankup_notification, rankup_mention)

    # /send delete
    @app_commands.command(name="delete",description="指定された戦績を送信するプレイヤーを削除します。 / The War record send player delete.")
    async def send_delete(self, interaction: discord.Interaction,lounge_name:str):

        await delete().delete_info(interaction, lounge_name)

    # /send list
    @app_commands.command(name="list",description="戦績を送信するために登録されているプレイヤーを表示します。 / The War record send player list view.")
    async def send_list(self, interaction: discord.Interaction):

        await list().list_info(interaction)

async def setup(bot: commands.Bot):
    bot.tree.add_command(send(bot, name="send"))