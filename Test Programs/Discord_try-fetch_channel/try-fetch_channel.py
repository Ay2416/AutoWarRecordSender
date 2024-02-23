# Discord bot import
import discord
from discord import app_commands
from discord import ui
from discord.ext import tasks
import os
from dotenv import load_dotenv
import glob
import ndjson
import time
import datetime
import dateutil.parser
import requests

# Bot start
load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("接続しました！")
    # await client.change_presence(activity=discord.Game(name="/help"))

    #await tree.sync()#スラッシュコマンドを同期
    #print("グローバルコマンド同期完了！")
    await tree.sync(guild=discord.Object(your_guild_id)) 
    print("ギルドコマンド同期完了！")

# /help
@tree.command(name="help",description="コマンドについての簡単な使い方を出します。")
@discord.app_commands.guilds(your_guild_id)
async def help(interaction: discord.Interaction, channel:discord.TextChannel):
        print(channel.id)

        try:
            await client.fetch_channel(channel.id)
        except discord.errors.InvalidData:
            print("エラー！:discord.errors.InvaliData")
            embed=discord.Embed(title="エラー！", description="Discord Api側から定義されていないチャンネルタイプが受信されました！", color=0xff0000)
            embed.add_field(name="※詳細↓", value="https://discordpy.readthedocs.io/ja/latest/api.html#discord.Client.fetch_channel", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except discord.errors.HTTPException:
            print("エラー！:discord.errors.HTTPException")
            embed=discord.Embed(title="エラー！", description="チャンネルの取得に失敗しました。\nこのチャンネルを見る権限がありません！\nもしこのチャンネルを指定したい場合はBotが見られるように権限を設定する必要があります。", color=0xff0000)
            embed.add_field(name="※詳細↓", value="https://discordpy.readthedocs.io/ja/latest/api.html#discord.Client.fetch_channel", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except discord.errors.NotFound:
            print("エラー！:discord.errors.InvaliData")
            embed=discord.Embed(title="エラー！", description="チャンネルIDが無効です！（※指定したチャンネルがこのサーバーの者ではない可能性があります。）", color=0xff0000)
            embed.add_field(name="※詳細↓", value="https://discordpy.readthedocs.io/ja/latest/api.html#discord.Client.fetch_channel", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except discord.errors.Forbidden:
            print("エラー！:discord.errors.Forbidden")
            embed=discord.Embed(title="エラー！", description="このチャンネルを見る権限がありません！\nもしこのチャンネルを指定したい場合はBotが見られるように権限を設定する必要があります。", color=0xff0000)
            embed.add_field(name="※詳細↓", value="hhttps://discordpy.readthedocs.io/ja/latest/api.html#discord.Client.fetch_channel", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        else:
            embed=discord.Embed(title="成功しました！", description="OK!", color=0xffffff)
            await interaction.response.send_message(embed=embed, ephemeral=False)

client.run(os.environ['token'])
