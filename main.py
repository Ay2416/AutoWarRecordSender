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
#from time import sleep
import asyncio
import math

# Bot start
load_dotenv()
update_time =  300 # 更新間隔を設定（秒）
delay_time = 15 # /send_add,/send_deleteの使える間隔の設定（秒）
api_url = "https://www.mk8dx-lounge.com/api/player/details?name="
api_url_id = "https://www.mk8dx-lounge.com/api/player/details?id="
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
UTC = datetime.timezone(datetime.timedelta(hours=0), 'UTC')


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("接続しました！")
    # await client.change_presence(activity=discord.Game(name="/help"))

    await tree.sync()#スラッシュコマンドを同期
    print("グローバルコマンド同期完了！")
    
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
    war_record_send.start()
    print("戦績の確認を開始します！")

# サーバーに招待された場合に特定の処理をする
@client.event
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
@client.event
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
async def war_record_send():   
    # guild_jsonのファイル一覧を取得
    files = glob.glob('./guild_json/' + '*.ndjson')
    
    # 戦績の更新があるかどうかを確認する処理
    for i in range(0, len(files)):
        #print("a")
        hozon = 1 # 戦績結果の更新をする回数を保存する用

        # 言語の確認
        with open('./language_json/' + os.path.split(files[i])[1]) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        with open('./guild_json/' + os.path.split(files[i])[1]) as f:
                read_data = ndjson.load(f)
        
        for j in range(0, len(read_data)):
            #print("i")
            # apiサーバー気休めのためのディレイをかける
            await asyncio.sleep(2)

            # 設定されている更新時間がきているかどうかの判定
            now = time.time() # メンテ時はありえないほど小さい数字を入れる
            if(read_data[j]["latest_time"] + update_time <= now):
                response =  requests.get(api_url_id + str(read_data[j]["playerId"]))
                result = response.json()

                #print(response.status_code)
                if response.status_code != 200:
                    print("ラウンジのサーバーが落ちている可能性がある判定でcontinueしました")
                    continue

                # data_jsonフォルダからラウンジapiの古い情報を取得
                with open('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(read_data[j]["playerId"]) + ".ndjson") as f:
                    read_data2 = ndjson.load(f)
                
                print(str(read_data2[0]["playerId"]) + "の処理を開始します")

                old_info = read_data2[0]["mmrChanges"]
                new_info = result["mmrChanges"]
                
                # Placement（ラウンジを始めたばっかりの人）やシーズンが始まったばっかりの時に動く判定処理
                if len(new_info) == 1 or len(new_info) == 0:
                    
                    if read_data[j]["season_alert"] == 0 or read_data[j]["season_alert"] == 1:
                        if len(new_info) == 1:
                            # メンションが必要であるか
                            if read_data[j]["mention"] != "null":
                                channel_sent = client.get_channel(read_data[j]["channel"])

                                try:
                                    await channel_sent.send("<@" + read_data[j]["mention"] + ">")
                                except Exception as e:
                                    guild = client.get_guild(int(os.path.splitext(os.path.basename(files[i]))[0]))
                                    user = await client.fetch_user(int(read_data[j]["mention"]))
                                    if language == "ja":
                                        embed=discord.Embed(title="送信エラー",description= guild.name + "のサーバーでメッセージを送信することができませんでした。\nこの通知がしばらく続く場合は、サポートサーバーへ連絡を入れてください。", color=0x00008b)
                                    elif language == "en":
                                        embed=discord.Embed(title="Send Error", description="A message could not be sent on " + guild.name + "server.\nIf this notification persists for some time, please contact our support server.", color=0x00008b)
                                    
                                    await user.send(embed=embed)

                                    print("mentionエラーでcontinueしました。")
                                    continue
                            
                            if language == "ja":
                                embed=discord.Embed(title="データがありません！\n新しいユーザーであるか、もしくは新シーズンが始まります！\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
                            elif language == "en":
                                embed=discord.Embed(title="No data!\nNew User or New Season!\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
                            
                            # 更新された日付・時刻を格納→変換
                            if language == "ja":
                                date = dateutil.parser.parse(new_info[0]["time"]).astimezone(JST)
                                embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " JST", value="", inline=False)
                            elif language == "en":
                                date = dateutil.parser.parse(new_info[0]["time"]).astimezone(UTC)
                                embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " UTC", value="", inline=False)  
                            embed.add_field(name="Now mmr:  " + str(new_info[0]["newMmr"]), value=" ", inline=True)
                            if language == "ja":
                                embed.add_field(name="・詳細をサイトで見る", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=False)
                            elif language == "en":
                                embed.add_field(name="・View detail", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=False)
                            
                            channel_sent = client.get_channel(read_data[j]["channel"])
                            await channel_sent.send(embed=embed)
                            read_data[j]["season_alert"] = 2

                        elif len(new_info) == 0 and read_data[j]["season_alert"] == 0:
                            # メンションが必要であるか
                            if read_data[j]["mention"] != "null":
                                channel_sent = client.get_channel(read_data[j]["channel"])

                                try:
                                    await channel_sent.send("<@" + read_data[j]["mention"] + ">")
                                except Exception as e:
                                    guild = client.get_guild(int(os.path.splitext(os.path.basename(files[i]))[0]))
                                    user = await client.fetch_user(int(read_data[j]["mention"]))
                                    if language == "ja":
                                        embed=discord.Embed(title="送信エラー",description= guild.name + "のサーバーでメッセージを送信することができませんでした。\nこの通知がしばらく続く場合は、サポートサーバーへ連絡を入れてください。\nhttps://discord.gg/CVXXPdk8", color=0x00008b)
                                    elif language == "en":
                                        embed=discord.Embed(title="Send Error", description="A message could not be sent on " + guild.name + "server.\nIf this notification persists for some time, please contact our support server.\nhttps://discord.gg/CVXXPdk8", color=0x00008b)
                                    
                                    await user.send(embed=embed)

                                    print("mentionエラーでcontinueしました。")
                                    continue
                            
                            if language == "ja":
                                embed=discord.Embed(title="データがありません！\n新しいユーザーであるか、もしくは新シーズンが始まります！\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
                            elif language == "en":
                                embed=discord.Embed(title="No data!\nNew User or New Season!\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
                            
                            embed.add_field(name="No data.", value=" ", inline=True)
                            if language == "ja":
                                embed.add_field(name="・詳細をサイトで見る", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=False)
                            elif language == "en":
                                embed.add_field(name="・View detail", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=False)
                            
                            channel_sent = client.get_channel(read_data[j]["channel"])
                            await channel_sent.send(embed=embed)
                            read_data[j]["season_alert"] = 1 
                    
                    # read_data2に最新の情報を書きこむ
                    os.remove('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(read_data[j]["playerId"]) + ".ndjson")
                    with open('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(result["playerId"]) + ".ndjson", 'a') as f:
                        writer = ndjson.writer(f)
                        writer.writerow(result)

                    '''
                    # 名前に変更があった場合、read_dataの名前を変更する
                    if result["name"] != read_data[j]["name"]:
                        read_data[j]["name"] = result["name"]
                    '''
                    
                    # read_dataのlatest_timeを更新
                    read_data[j]["latest_time"] = time.time()

                    os.remove('./guild_json/' + os.path.split(files[i])[1])
                    for k in range(0, len(read_data)):
                        with open('./guild_json/' + os.path.split(files[i])[1], 'a') as f:
                            writer = ndjson.writer(f)
                            writer.writerow(read_data[k])
                    
                    print("Placement（ラウンジを始めたばっかりの人）やシーズンが始まったばっかりの時に動く判定でcontinueしました")
                    
                    continue
                
                #print(read_data[j]["name"])
                #print(len(new_info))
                #print(len(old_info))
                #channel_sent = client.get_channel(1090113806174273606) # debug
                #await channel_sent.send(len(new_info)) # debug
                if len(old_info) == 0: # reason:Placement（api上）を抜けて、1回目の模擬をやった人が通過する用
                    hozon = len(new_info) - (len(new_info) - 1) 
                elif old_info[0]["reason"] == "Placement": # new_infoが0、1じゃないときの処理（reason:Placement（api上）を抜け、2回以上やった人）
                    hozon = len(new_info) - 1
                else:
                    try:
                        for k in range(0, len(new_info)):
                            if old_info[0]["changeId"] == new_info[k]["changeId"]:
                                hozon = k
                                break
                    except Exception as e:
                        hozon = 1
                        
                        print("何かエラーが発生したため、hozon = 1としました")
                #print(hozon)
                if hozon == 0:
                    # read_data2に最新の情報を書きこむ
                    os.remove('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(read_data[j]["playerId"]) + ".ndjson")
                    with open('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(result["playerId"]) + ".ndjson", 'a') as f:
                        writer = ndjson.writer(f)
                        writer.writerow(result)

                    '''
                    # 名前に変更があった場合、read_dataの名前を変更する
                    if result["name"] != read_data[j]["name"]:
                        read_data[j]["name"] = result["name"]
                    '''
                    
                    # read_dataのlatest_timeを更新
                    read_data[j]["latest_time"] = time.time()

                    os.remove('./guild_json/' + os.path.split(files[i])[1])
                    for k in range(0, len(read_data)):
                        with open('./guild_json/' + os.path.split(files[i])[1], 'a') as f:
                            writer = ndjson.writer(f)
                            writer.writerow(read_data[k])
                    
                    print("hozon = 0の判定でcontinueしました")
                    continue
                
                for l in range(hozon-1,-1,-1):
                    #print(l)

                    # ランクを判定する season9時点のランクを入れておく seasonが変わることに確認する必要あり
                    rank_num = new_info[l]["newMmr"]

                    if rank_num >= 17000:
                        rank = "Grandmaster"
                    elif rank_num >= 16000:
                        rank = "Master"
                    elif rank_num >= 15000:
                        rank = "Diamond 2"
                    elif rank_num >= 14000:
                        rank = "Diamond 1"
                    elif rank_num >= 13000:
                        rank = "Ruby 2"
                    elif rank_num >= 12000:
                        rank = "Ruby 1"
                    elif rank_num >= 11000:
                        rank = "Sapphire 2"
                    elif rank_num >= 10000:
                        rank = "Sapphire 1"
                    elif rank_num >= 9000:
                        rank = "Platinum 2"
                    elif rank_num >= 8000:
                        rank = "Platinum 1"
                    elif rank_num >= 7000:
                        rank = "Gold 2"
                    elif rank_num >= 6000:
                        rank = "Gold 1"
                    elif rank_num >= 5000:
                        rank = "Silver 2"
                    elif rank_num >= 4000:
                        rank = "Silver 1"
                    elif rank_num >= 3000:
                        rank = "Bronze 2"
                    elif rank_num >= 2000:
                        rank = "Bronse 1"
                    elif rank_num >= 1000:
                        rank = "Iron 2"
                    elif rank_num >= 0:
                        rank = "Iron 1"
                    #else:
                    #    rank = "Placement"

                    # mmrDeltaに+の数値であれば+を付ける判定
                    if new_info[l]["mmrDelta"] > 0:
                        mmrdelta = "+" + str(new_info[l]["mmrDelta"])
                    else:
                        mmrdelta = str(new_info[l]["mmrDelta"])

                    if read_data[j]["mention"] != "null":
                        channel_sent = client.get_channel(read_data[j]["channel"])

                        try:
                            await channel_sent.send("<@" + read_data[j]["mention"] + ">")
                        except Exception as e:
                            guild = client.get_guild(int(os.path.splitext(os.path.basename(files[i]))[0]))
                            user = await client.fetch_user(int(read_data[j]["mention"]))
                            if language == "ja":
                                embed=discord.Embed(title="送信エラー",description= guild.name + "のサーバーでメッセージを送信することができませんでした。\nこの通知がしばらく続く場合は、サポートサーバーへ連絡を入れてください。", color=0x00008b)
                            elif language == "en":
                                embed=discord.Embed(title="Send Error", description="A message could not be sent on " + guild.name + "server.\nIf this notification persists for some time, please contact our support server.", color=0x00008b)
                            
                            await user.send(embed=embed)

                            print("mentionエラーでcontinueしました。")
                            continue
            
                    if language == "ja":
                        embed=discord.Embed(title="戦績が更新されました！\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
                    elif language == "en":
                        embed=discord.Embed(title="Update War Record！\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
                    # 更新された日付・時刻を格納→変換
                    if language == "ja":
                        date = dateutil.parser.parse(new_info[0]["time"]).astimezone(JST)
                        embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " JST", value="", inline=False)
                    elif language == "en":
                        date = dateutil.parser.parse(new_info[0]["time"]).astimezone(UTC)
                        embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " UTC", value="", inline=False)    
                    embed.add_field(name="mmr:  " + str(new_info[l]["newMmr"]), value=" ", inline=True)
                    embed.add_field(name="+ / - :  " + mmrdelta, value=" ", inline=True)
                    embed.add_field(name="Now Rank:  " + rank, value=" ", inline=True)
                    if language == "ja":
                        embed.add_field(name="・詳細をサイトで見る", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=True)
                    elif language == "en":
                        embed.add_field(name="・View detail", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=True)
                    embed.set_image(url="https://www.mk8dx-lounge.com/TableImage/" + str(new_info[l]["changeId"]) + ".png")
                    
                    # channel idを抽出する
                    #id = read_data[j]["channel"]
                    #id = id[2:]
                    #id = id[:-1]
                    
                    channel_sent = client.get_channel(read_data[j]["channel"])
                    await channel_sent.send(embed=embed)
                
                # read_data2に最新の情報を書きこむ
                os.remove('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(read_data[j]["playerId"]) + ".ndjson")
                with open('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(result["playerId"]) + ".ndjson", 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(result)
                
                '''
                # 名前に変更があった場合、read_dataの名前を変更する
                if result["name"] != read_data[j]["name"]:
                    read_data[j]["name"] = result["name"]
                '''
                
                # season_alertの初期化処理
                if len(new_info) > 1 and read_data[j]["season_alert"] >= 1:
                    read_data[j]["season_alert"] = 0
                
                # read_dataのlatest_timeを更新
                read_data[j]["latest_time"] = time.time()

                os.remove('./guild_json/' + os.path.split(files[i])[1])
                for k in range(0, len(read_data)):
                    with open('./guild_json/' + os.path.split(files[i])[1], 'a') as f:
                        writer = ndjson.writer(f)
                        writer.writerow(read_data[k])
                
                print("表示し、更新する所までの処理を全て正常に通過しました")
        print(os.path.splitext(os.path.basename(files[i]))[0] + "のサーバーの処理が終了しました")

#Bot commands

# /send add
@tree.command(name="send_add",description="戦績を送信するプレイヤーを追加します。 / The War record send player add.")
@discord.app_commands.choices(mention=[discord.app_commands.Choice(name="on",value="on"),discord.app_commands.Choice(name="off",value="off")])
async def send_add(interaction: discord.Interaction,lounge_name:str,channel:discord.TextChannel,mention:str):
    await interaction.response.defer(ephemeral=True)
    # 言語の確認
    file = str(interaction.guild.id) + ".ndjson"

    with open('./language_json/' + file) as f:
        read_data = ndjson.load(f)

    language = read_data[0]["language_mode"]

    # 最後に/send_add,/send_deleteを使ったからn秒空いているかの確認
    files = glob.glob('./delay_json/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson":
            judge = 1
            break
        
    if judge == 1:
        with open('./delay_json/' + str(interaction.guild.id) + '.ndjson') as f:
            read_data = ndjson.load(f)
        
        now = time.time()
        if read_data[0]["time"] + delay_time >= now:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description="コマンドクールタイムです！\nコマンドが使用可能になるまであと " + str(math.ceil((read_data[0]["time"] + delay_time) - now)) + " 秒お待ちください！", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description="Command cool time!\n Please " + str(math.ceil((read_data[0]["time"] + delay_time) - now)) + " seconds wait!", color=0xff0000)
            
            await interaction.followup.send(embed=embed)
            return
            
        os.remove('./delay_json/' + str(interaction.guild.id) + '.ndjson')
        content = {
            "time" : time.time()
        }

        with open('./delay_json/' + str(interaction.guild.id) + '.ndjson', 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(content)
            
    else:
        #os.remove('./delay_json/' + str(interaction.guild.id) + '.ndjson')
        content = {
            "time" : time.time()
        }

        with open('./delay_json/' + str(interaction.guild.id) + '.ndjson', 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(content)

    # ループ処理と処理が被って予期しないエラーにならないための処理
    #war_record_send.stop()
    #await asyncio.sleep(3)

    '''
    print(channel.id)
    #print(lounge_name + " " + channel)

    try:
        await client.fetch_channel(channel.id)
    except discord.errors.InvalidData:
        print("エラー！:discord.errors.InvaliData")
        embed=discord.Embed(title="エラー！", description="Discord Api側から定義されていないチャンネルタイプが受信されました！", color=0xff0000)
        embed.add_field(name="※詳細↓", value="https://discordpy.readthedocs.io/ja/latest/api.html#discord.Client.fetch_channel", inline=False)
        await interaction.followup.send(embed=embed)
        return
    except discord.errors.HTTPException:
        print("エラー！:discord.errors.HTTPException")
        embed=discord.Embed(title="エラー！", description="チャンネルの取得に失敗しました。\nこのチャンネルを見る権限がありません！\nもしこのチャンネルを指定したい場合はBotが見られるように権限を設定する必要があります。", color=0xff0000)
        embed.add_field(name="※詳細↓", value="https://discordpy.readthedocs.io/ja/latest/api.html#discord.Client.fetch_channel", inline=False)
        await interaction.followup.send(embed=embed)
        return
    except discord.errors.NotFound:
        print("エラー！:discord.errors.InvaliData")
        embed=discord.Embed(title="エラー！", description="チャンネルIDが無効です！（※指定したチャンネルがこのサーバーの者ではない可能性があります。）", color=0xff0000)
        embed.add_field(name="※詳細↓", value="https://discordpy.readthedocs.io/ja/latest/api.html#discord.Client.fetch_channel", inline=False)
        await interaction.followup.send(embed=embed)
        return
    except discord.errors.Forbidden:
        print("エラー！:discord.errors.Forbidden")
        embed=discord.Embed(title="エラー！", description="このチャンネルを見る権限がありません！\nもしこのチャンネルを指定したい場合はBotが見られるように権限を設定する必要があります。", color=0xff0000)
        embed.add_field(name="※詳細↓", value="hhttps://discordpy.readthedocs.io/ja/latest/api.html#discord.Client.fetch_channel", inline=False)
        await interaction.followup.send(embed=embed)
        return
    else:
        pass
    '''

    if mention == "on" or mention == "off":
        print("成功！:メンションの設定通過！")
    else:
        print("エラー！:コマンドのメンションの設定が間違っています！ご確認ください。")
        if language == "ja":
            embed=discord.Embed(title="エラー！", description="コマンドのメンションの指定が間違っています！\nご確認ください。", color=0xff0000)
        elif language == "en":
            embed=discord.Embed(title="Error!", description="Command mention setting error!\nCheck typing keyword. ([on] or [off])", color=0xff0000)
        await interaction.followup.send(embed=embed)
        return
    
    response =  requests.get(api_url + lounge_name)
    
    #print(response.status_code)
    if response.status_code != 200:
        print("エラー！:このラウンジの名前は存在しません！")
        if language == "ja":
            embed=discord.Embed(title="エラー！", description="このラウンジの名前は存在しません！", color=0xff0000)
        elif language == "en":
            embed=discord.Embed(title="Error!", description="This Lounge name not found!", color=0xff0000)     
        await interaction.followup.send(embed=embed)
        return

    result = response.json()

    print(result["name"])
    #print(channel[0:1])
    #if channel[0:2] != "<#":
    #    print("エラー！:これはチャンネルではありません！")
    #    embed=discord.Embed(title="エラー！", description="これはチャンネルではありません！", color=0xff0000)
    #    await interaction.followup.send(embed=embed)
    #    return       

    # 既にデータ保存用のディレクトリが存在しているかの確認
    judge = 0
    dir_data = os.listdir(path='./data_json')
    for i in range(0, len(dir_data)):
        if str(interaction.guild.id) == dir_data[i]:
            judge = 1
            break

    if judge != 1: # なければ作成する
        os.mkdir('./data_json/' + str(interaction.guild.id))
    
    # 指定のユーザーのndjsonファイルが存在しているかの確認
    files = glob.glob('./data_json/' + str(interaction.guild.id) + '/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == str(result["playerId"]) + ".ndjson"):
            #print("一致しました！")
            judge = 1
            break
    
    if judge != 1:
        # print(interaction.guild.id)

        with open('./data_json/' + str(interaction.guild.id) + '/' + str(result["playerId"]) + ".ndjson", 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(result)
    else:
        #file = str(interaction.guild.id) + ".ndjson"
        with open('./data_json/' + str(interaction.guild.id) + '/' + str(result["playerId"]) + ".ndjson") as f:
                    read_data = ndjson.load(f)
        
        judge = 1
        for i in range(0, len(read_data)):
            if result["name"] == read_data[i]["name"]:
                judge = 0
                break
        
        if judge == 0:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:既に同じ名前の人が登録されています。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:This name is already registered.:x:", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return

    # メンション用の処理
    user = ""
    if mention == "on":
        user = str(interaction.user.id)
    else:
        user = "null"
    
    # guild_jsonフォルダにサーバーidのフォルダを作成
    content = {
            "playerId" : result["playerId"],
            "latest_time": time.time(),
            "channel": channel.id,
            "season_alert": 0,
            "mention": user
    }

    with open('./guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
        writer = ndjson.writer(f)
        writer.writerow(content)

    #war_record_send.start()

    print("登録しました!:" + result["name"] + "として入力された内容を保存しました。")
    if language == "ja":
        embed=discord.Embed(title="登録しました!", description=result["name"] + "さんを追加しました。", color=0x00ff7f)
    elif language == "en":
        embed=discord.Embed(title="Registered!", description=result["name"] + " added.", color=0x00ff7f)        
    await interaction.followup.send(embed=embed)

    #await interaction.response.send_message(text, ephemeral=False)

# /send delete
@tree.command(name="send_delete",description="指定された戦績を送信するプレイヤーを削除します。 / The War record send player delete.")
async def send_delete(interaction: discord.Interaction,lounge_name:str):
    await interaction.response.defer(ephemeral=True)

    # 言語の確認
    file = str(interaction.guild.id) + ".ndjson"

    with open('./language_json/' + file) as f:
        read_data = ndjson.load(f)

    language = read_data[0]["language_mode"]

    # 最後に/send_add,/send_deleteを使ったからn秒空いているかの確認
    files = glob.glob('./delay_json/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson":
            judge = 1
            break
    
    print(judge)
    if judge == 1:
        with open('./delay_json/' + str(interaction.guild.id) + '.ndjson') as f:
            read_data = ndjson.load(f)
        
        now = time.time()
        if read_data[0]["time"] + delay_time >= now:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description="コマンドクールタイムです！\nコマンドが使用可能になるまであと " + str(math.ceil((read_data[0]["time"] + delay_time) - now)) + " 秒お待ちください！", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description="Command cool time!\n Please " + str(math.ceil((read_data[0]["time"] + delay_time) - now)) + " seconds wait!", color=0xff0000)
            
            await interaction.followup.send(embed=embed)
            return
            
        os.remove('./delay_json/' + str(interaction.guild.id) + '.ndjson')
        content = {
            "time" : time.time()
        }

        with open('./delay_json/' + str(interaction.guild.id) + '.ndjson', 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(content)
            
    else:
        #os.remove('./delay_json/' + str(interaction.guild.id) + '.ndjson')
        content = {
            "time" : time.time()
        }

        with open('./delay_json/' + str(interaction.guild.id) + '.ndjson', 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(content)

    # ループ処理と処理が被って予期しないエラーにならないための処理
    #war_record_send.stop()
    #await asyncio.sleep(3)
    
    #print(lounge_name)

    response =  requests.get(api_url + lounge_name)
    result = response.json()
    
    #print(response.status_code)
    if response.status_code != 200:
        print("エラー！:このラウンジの名前は存在しません！")
        if language == "ja":
            embed=discord.Embed(title="エラー！", description="このラウンジの名前は存在しません！", color=0xff0000)
        elif language == "en":
            embed=discord.Embed(title="Error!", description="This Lounge name not found!", color=0xff0000)   
        await interaction.followup.send(embed=embed)
        return

    # 既にデータ保存用のディレクトリが存在しているかの確認
    judge = 0
    dir_data = os.listdir(path='./data_json')
    for i in range(0, len(dir_data)):
        if str(interaction.guild.id) == dir_data[i]:
            judge = 1
            break

    if judge != 1: # なければエラー
        if language == "ja":
            embed=discord.Embed(title="エラー!", description=":x:このサーバーのデータがありません。:x:", color=0xff0000)
        elif language == "en":
            embed=discord.Embed(title="Error!", description=":x:This server is no data.:x:", color=0xff0000)
        await interaction.followup.send(embed=embed)
        return
    
    # 指定のユーザーのndjsonファイルが存在しているかの確認
    files = glob.glob('./data_json/' + str(interaction.guild.id) + '/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == str(result["playerId"]) + ".ndjson"):
            #print("一致しました！")
            judge = 1
            break
    
    if judge != 1:
        if language == "ja":
            embed=discord.Embed(title="エラー!", description=":x:指定されたユーザーのデータがありません。:x:", color=0xff0000)
        elif language == "en":
            embed=discord.Embed(title="Error!", description=":x:User data not found.:x:", color=0xff0000)           
        await interaction.followup.send(embed=embed)
        return
    
    # data_jsonファルダにあるユーザーデータの削除
    os.remove('./data_json/' + str(interaction.guild.id) + '/' + str(result["playerId"]) + ".ndjson")

    # data_jsonフォルダ内のサーバーフォルダの中身がなくなりそうな場合にフォルダを削除する
    if len(files) == 1:
        os.rmdir('./data_json/' + str(interaction.guild.id))
    
    # guild_jsonフォルダにある、サーバーidのndjsonフォルダから、ユーザーデータの削除
    with open('./guild_json/' + str(interaction.guild.id) + ".ndjson") as f:
        read_data = ndjson.load(f)
                
    if len(read_data) == 1:
        os.remove('./guild_json/' + str(interaction.guild.id) + ".ndjson")
    else:
        data_location = 0
        print(read_data)
        for i in range(0, len(read_data)):
            if result["playerId"] == read_data[i]["playerId"]:
                data_location = i
                #print(read_data)
                break

        #if data_write == 1:
        os.remove('./guild_json/' + str(interaction.guild.id) + ".ndjson")

        for i in range(0, len(read_data)):
            if i != data_location:
                with open('./guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(read_data[i])
    
    # war_record_send.start()
    
    print("削除成功！:" + lounge_name + "を削除しました。また利用する際には/send_addコマンドを使用して、追加してください。")
    if language == "ja":
        embed=discord.Embed(title="削除成功！", description=lounge_name + "さんを削除しました。\nまた利用する際には/send_addコマンドを使用して、追加してください。", color=0x00ff7f)
    elif language == "en":
        embed=discord.Embed(title="Deleted!", description=lounge_name + " deleted。\nWhen using it again, please use the /send_add command to add it.", color=0x00ff7f)
    await interaction.followup.send(embed=embed)
    #await interaction.response.send_message(text, ephemeral=False)

# /send list
@tree.command(name="send_list",description="戦績を送信するために登録されているプレイヤーを表示します。 / The War record send player list view.")
async def send_list(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)

    # 言語の確認
    file = str(interaction.guild.id) + ".ndjson"

    with open('./language_json/' + file) as f:
        read_data = ndjson.load(f)

    language = read_data[0]["language_mode"]

    # 指定のユーザーのndjsonファイルが存在しているかの確認
    files = glob.glob('./guild_json/*.ndjson')
    print(len(files))
    judge = 0

    for i in range(0, len(files)):
        print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
            #print("一致しました！")
            judge = 1
            break
    
    if judge != 1:
        if language == "ja":
            embed=discord.Embed(title="エラー!", description=":x:このサーバーには登録されているプレイヤーがいません。:x:", color=0xff0000)
        elif language == "en":
            embed=discord.Embed(title="Error!", description=":x:There are no registered players on this server.:x:", color=0xff0000)
        await interaction.followup.send(embed=embed)
        return
    
    with open('./guild_json/' + str(interaction.guild.id) + ".ndjson") as f:
        read_data = ndjson.load(f)
    
    if language == "ja":
        embed=discord.Embed(title="登録されているプレイヤー")
    elif language == "en":
        embed=discord.Embed(title="Registered Player")
    
    mention_setting = " "
    cut = 25
    for i in range(0, len(read_data)):
        if read_data[i]["mention"] != "null":
            mention_setting = "on"
        else:
            mention_setting = "off"

        with open('./data_json/' + str(interaction.guild.id) + '/' + str(read_data[i]["playerId"]) + '.ndjson') as f:
            read_data2 = ndjson.load(f)
        
        if language == "ja":
            embed.add_field(name=read_data2[0]["name"], value="投稿先チャンネル：<#" + str(read_data[i]["channel"]) + ">\nメンション：" + mention_setting, inline=False)
        elif language == "en":
            embed.add_field(name=read_data2[0]["name"], value="Send Channel: <#" + str(read_data[i]["channel"]) + ">\nMention: " + mention_setting, inline=False)
        
        if i == len(read_data) - 1:
            #表示させる
            await interaction.followup.send(embed=embed)
            return
        
        if i + 1 == cut:
            cut = cut + 25
            #表示させる
            await interaction.followup.send(embed=embed)
            embed=discord.Embed(title="")
            
            # DiscordのWebhook送信制限に引っかからないための対策　※効果があるかは不明
            await asyncio.sleep(2)

# /language
@tree.command(name="language",description="言語を変更します。（jaまたはen） / Change language. (ja or en)")
@discord.app_commands.choices(language=[discord.app_commands.Choice(name="ja",value="ja"),discord.app_commands.Choice(name="en",value="en")])
async def language_command(interaction: discord.Interaction,language:str):
    # 言語の確認
    file = str(interaction.guild.id) + ".ndjson"

    with open('./language_json/' + file) as f:
        read_data = ndjson.load(f)

    now_language = read_data[0]["language_mode"]

    # 登録されている言語かどうかの確認
    if language == "ja" or language == "en":
        print("成功！:登録されている言語です！")
    else:
        print("エラー！:コマンドの言語の設定が間違っています！ご確認ください。")
        if now_language == "ja":
            embed=discord.Embed(title="エラー！", description="コマンドの言語指定が間違っています！\nご確認ください。", color=0xff0000)
        elif now_language == "en":
            embed=discord.Embed(title="Error!", description="Command language setting error!\nCheck typing keyword. ([ja] or [en])", color=0xff0000)
        await interaction.response.send_message(embed=embed)
        return
    
    # 既にファイルが存在しているかの判定
    files = glob.glob('./language_json/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
            print("一致しました！")
            judge = 1
            break
        else:
            judge = 0
    
    file = str(interaction.guild.id) + ".ndjson"

    if(judge == 1):
        os.remove("./language_json/" + file)

    content = {
        "language_mode" : language
    }

    with open('./language_json/' + file, 'a') as f:
        writer = ndjson.writer(f)
        writer.writerow(content)

    # メッセージ表示
    if language == "ja":
        print(str(interaction.guild.id) + "の言語を日本語に変更しました。")
        embed=discord.Embed(title="成功しました!", description="日本語に変更しました。", color=0x00ff40)
        await interaction.response.send_message(embed=embed, ephemeral=False)
    elif language == "en":
        print(str(interaction.guild.id) + "の言語を英語に変更しました。")
        embed=discord.Embed(title="Success!", description="Change to English.", color=0x00ff40)
        await interaction.response.send_message(embed=embed, ephemeral=False)

# /help
@tree.command(name="help",description="コマンドについての簡単な使い方を出します。 / How to use command and Command list.")
async def help(interaction: discord.Interaction):
    # 言語の確認
    file = str(interaction.guild.id) + ".ndjson"

    with open('./language_json/' + file) as f:
        read_data = ndjson.load(f)

    language = read_data[0]["language_mode"]

    #Discord上にヘルプを表示
    if language == "ja":
        embed=discord.Embed(title="コマンドリスト")
        embed.add_field(name="/send_add [ラウンジ名] [投稿チャンネル（「#○○○」の形）] [メンションの有無（on/off）]", value="戦績を送信するプレイヤーを追加します。\nまた、メンション設定はオンにした場合、コマンドを入力したプレイヤーにメンションが行くように設定されます。\n※コマンドクールタイムが " + str(delay_time) + " 秒あります。（/send_add, /send_delteコマンド共通）", inline=False)
        embed.add_field(name="/send_delete [ラウンジ名]", value="戦績を送信するプレイヤーの削除を行います。\n※コマンドクールタイムが " + str(delay_time) + " 秒あります。（/send_add, /send_delteコマンド共通）", inline=False)
        embed.add_field(name="/send_list", value="戦績を送信する登録があるプレイヤーの一覧を表示します。", inline=False)
        embed.add_field(name="/language [言語の選択（ja/en）]", value="このBotのコマンドの言語を変更します。", inline=False)
        embed.add_field(name="/help", value="このBotのコマンドの簡単な使い方を出します。", inline=False)
    elif language == "en":
        embed=discord.Embed(title="Command list")
        embed.add_field(name="/send_add [Lounge name] [send Channel ([#○○○])] [Mention setting (on/off)]", value="The War Record send player add.\nIn addition, the Mention setting, when turned on, is set so that the ments go to the player who entered the command.\n※Command cool time" + str(delay_time) + " seconds. (/send_add, /send_delete command common)", inline=False)
        embed.add_field(name="/send_delete [Lounge name]", value="The War Record send player delete.\n※Command cool time" + str(delay_time) + " seconds. (/send_add, /send_delete command common)", inline=False)
        embed.add_field(name="/send_list", value="The War Record send player list view.", inline=False)
        embed.add_field(name="/language [language setting（ja/en）]", value="Change default language.", inline=False)
        embed.add_field(name="/help", value="How to use command and Command list.", inline=False)
    '''
    if interaction.guild.id == your_guild_id: # もしサーバー限定コマンドの実装があった場合の表記をした場合はここに書く
        embed.add_field(name="", value="", inline=False)
    '''
    await interaction.response.send_message(embed=embed,ephemeral=False)

client.run(os.environ['token'])
