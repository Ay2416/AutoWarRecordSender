# Discord bot import
import discord
from discord.ext import commands
from discord.ext import tasks
import os
#import traceback
from dotenv import load_dotenv
import glob
import ndjson
import asyncio

# My program import
from task import Task
from ContextMenu import ContextMenu

# Bot start
load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot起動時の処理（複数回行われる可能性あり）
@bot.event
async def on_ready():
    try:
        print("接続しました！")

        # await bot.change_presence(activity=discord.Game(name="/help"))
        
        # data_jsonフォルダがあるかの確認
        files = glob.glob('./*')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == "data_json"):
                print("data_jsonファイルを確認しました！")
                judge = 1
                break

        if judge != 1:
            os.mkdir('data_json')
            print("data_jsonファイルがなかったため作成しました！")

        # guild_jsonフォルダがあるかの確認
        judge = 0
        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == "guild_json"):
                print("guild_jsonファイルを確認しました！")
                judge = 1
                break

        if judge != 1:
            os.mkdir('guild_json')
            print("guild_jsonファイルがなかったため作成しました！")
        
        # delay_jsonフォルダがあるかの確認
        judge = 0
        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == "delay_json"):
                print("delay_jsonファイルを確認しました！")
                judge = 1
                break

        if judge != 1:
            os.mkdir('delay_json')
            print("delay_jsonファイルがなかったため作成しました！")
        
        # language_jsonフォルダがあるかの確認
        judge = 0
        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == "language_json"):
                print("language_jsonファイルを確認しました！")
                judge = 1
                break

        if judge != 1:
            os.mkdir('language_json')
            print("language_jsonファイルがなかったため作成しました！")

        # 定期的に動かすループ処理の開始
        #global channel_sent
        war_record_send_odd.start()
        print("（奇数）戦績の確認を開始します！")
        
        await asyncio.sleep(2)
        
        war_record_send_even.start()
        print("（偶数）戦績の確認を開始します！")
        
    except Exception as e:
        '''
        try:
            error_mention = "<@&" + str(your_role_id) + ">"
            embed=discord.Embed(title="タスクエラー",description="タスクでエラーが発生しました。\n```\n" + traceback.format_exc() + "\n```", color=0x00008b)
            channel_sent = bot.get_channel(your_channel_id)
            await channel_sent.send(error_mention, embed=embed)
        except Exception as e:
            error_mention = "<@&" + str(your_role_id) + ">"
            embed=discord.Embed(title="タスクエラー",description="タスクでエラーが発生しました。\nただしエラー文が制限文字数を超えたため、エラー文を送信することができませんでした。", color=0x00008b)
            channel_sent = bot.get_channel(your_channel_id)
            await channel_sent.send(error_mention, embed=embed)
        '''

        print("起動でエラーが発生しました。")

# Bot起動時の処理（起動時1回のみ実行）
@bot.event
async def setup_hook():
    try:
        # スラッシュコマンドを同期
        await bot.load_extension("Cogs.send")
        await bot.load_extension("Cogs.other")

        await bot.tree.sync()
        print("グローバルコマンド同期完了！")

        #await bot.tree.sync(guild=discord.Object(your_guild_id))
        #print("ギルドコマンド同期完了！")

    except Exception as e:
        '''
        try:
            error_mention = "<@&" + str(your_role_id) + ">"
            embed=discord.Embed(title="タスクエラー",description="タスクでエラーが発生しました。\n```\n" + traceback.format_exc() + "\n```", color=0x00008b)
            channel_sent = bot.get_channel(your_channel_id)
            await channel_sent.send(error_mention, embed=embed)
        except Exception as e:
            error_mention = "<@&" + str(your_role_id) + ">"
            embed=discord.Embed(title="タスクエラー",description="タスクでエラーが発生しました。\nただしエラー文が制限文字数を超えたため、エラー文を送信することができませんでした。", color=0x00008b)
            channel_sent = bot.get_channel(your_channel_id)
            await channel_sent.send(error_mention, embed=embed)
        '''

        print("起動でエラーが発生しました。")

# サーバーに招待された場合に特定の処理をする
@bot.event
async def on_guild_join(guild):
    file = str(guild.id) + ".ndjson"

    content = {
        "language_mode" : "ja"
    }

    with open('./language_json/' + file, 'a') as f:
        writer = ndjson.writer(f)
        writer.writerow(content)
    
    print("招待されたため" + str(guild.id) + "のlanguage jsonを作成しました。")

# サーバーからキック、BANされた場合に特定の処理をする
@bot.event
async def on_guild_remove(guild):
    file = str(guild.id) + ".ndjson"
    os.remove("./language_json/" + file)

    print("キックまたはBANされたため、" + str(guild.id) + "のlanguage jsonを削除しました。")
    
    files = glob.glob('./guild_json/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(guild.id) + ".ndjson":
            judge = 1
            break
    
    if judge == 1:
        os.remove("./guild_json/" + file)
        print("キックまたはBANされたため、" + str(guild.id) + "のguild jsonを削除しました。")
    
    files = glob.glob('./delay_json/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(guild.id) + ".ndjson":
            judge = 1
            break
    
    if judge == 1:
        os.remove("./delay_json/" + file)
        print("キックまたはBANされたため、" + str(guild.id) + "のdelay jsonを削除しました。")

    files = glob.glob('./data_json/*')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(guild.id):
            judge = 1
            break
    
    if judge == 1:
        os.remove("./data_json/" + str(guild.id) + "/" )
        print("キックまたはBANされたため、" + str(guild.id) + "のdata jsonを削除しました。")

#定期的に動かす処理（リマインダー的な）
@tasks.loop(seconds=60)
async def war_record_send_odd():
    await Task().send_message(bot, 1)        

@tasks.loop(seconds=60)
async def war_record_send_even():
    await Task().send_message(bot, 2)

# Context Menu コマンド
@bot.tree.context_menu(name='Add Send')
#@discord.app_commands.guilds(int(os.environ.get('Test_server')))
async def output_description(interaction: discord.Interaction, member:discord.User):
    await ContextMenu().add_send_program(interaction, member)

# Cogsに分けることができなかったコマンド（2023.8.13）
'''
# /war_record_odd_restart
@bot.tree.command(name="war_record_odd_restart",description="※Bot管理者用コマンド。 / ※Bot Admin command.")
@discord.app_commands.guilds(your_guild_id)
@discord.app_commands.default_permissions(administrator=True)
async def war_record_odd_restart(interaction: discord.Interaction):
    #戦績処理の再スタート
    war_record_send_odd.start()

    embed=discord.Embed(title="（奇数）戦績の確認をリスタートします。")
    embed.add_field(name="完了！", value=" ", inline=False)

    await interaction.response.send_message(embed=embed,ephemeral=False)

# /war_record_even_restart
@bot.tree.command(name="war_record_even_restart",description="※Bot管理者用コマンド。 / ※Bot Admin command.")
@discord.app_commands.guilds(your_guild_id)
@discord.app_commands.default_permissions(administrator=True)
async def war_record_even_restart(interaction: discord.Interaction):
    #戦績処理の再スタート
    war_record_send_even.start()

    embed=discord.Embed(title="（偶数）戦績の確認をリスタートします。")
    embed.add_field(name="完了！", value=" ", inline=False)

    await interaction.response.send_message(embed=embed,ephemeral=False)
'''


'''
# /fix_data
@bot.tree.command(name="fix_data",description="※Bot管理者用コマンド。 / ※Bot Admin command.")
@discord.app_commands.guilds(your_guild_id)
@discord.app_commands.default_permissions(administrator=True)
@discord.app_commands.choices(file_remove=[discord.app_commands.Choice(name="on",value="on"),discord.app_commands.Choice(name="off",value="off")])
async def fix_data(interaction: discord.Interaction, directory:str, player_id:str, file_remove:str):

    if interaction.user.id == your_user_id:
        try:    
            # データの取得
            api_url_id = "https://www.mk8dx-lounge.com/api/player/details?id="

            response =  requests.get(api_url_id + player_id)
            result = response.json()

            if file_remove == "on":
                os.remove(directory + player_id + ".ndjson")

            with open(directory + player_id + ".ndjson", 'a') as f:
                writer = ndjson.writer(f)
                writer.writerow(result)


            embed=discord.Embed(title="書き込み完了！")
            embed.add_field(name=directory + player_id + ".ndjsonを修正しました。", value=" ", inline=False)
        except Exception as e:
            embed=discord.Embed(title="エラー！", description="コマンドのエラーが発生しました。", color=0xff0000)
    else:
            embed=discord.Embed(title="エラー！", description="Botの管理者以外使用することができません。", color=0xff0000)

    await interaction.response.send_message(embed=embed,ephemeral=False)
'''

bot.run(os.environ['token'])
