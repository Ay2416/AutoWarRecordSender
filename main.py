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

# Bot start
load_dotenv()
update_time =  300 # 更新間隔を設定（秒）
api_url = "https://www.mk8dx-lounge.com/api/player/details?name="
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("接続しました！")

    await tree.sync()#スラッシュコマンドを同期
    print("グローバルコマンド同期完了！")
    
    # data_json, guild_jsonフォルダがあるかの確認
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

    judge = 0
    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == "guild_json"):
            print("guild_jsonファイルを確認しました！")
            judge = 1
            break

    if judge != 1:
        os.mkdir('guild_json')

    #戦績の更新確認のスタート
    war_record_send.start()
    print("戦績の確認を開始します！")

#定期的に動かす処理（リマインダー的な）
@tasks.loop(seconds=60)
async def war_record_send():   
    # guild_jsonのファイル一覧を取得
    files = glob.glob('./guild_json/' + '*.ndjson')
    
    # 戦績の更新があるかどうかを確認する処理
    for i in range(0, len(files)):
        hozon = 1 # 戦績結果の更新をする回数を保存する用
        with open('./guild_json/' + os.path.split(files[i])[1]) as f:
                read_data = ndjson.load(f)
        
        for j in range(0, len(read_data)):
            # apiサーバー気休めのためのディレイをかける
            await asyncio.sleep(2)

            # 設定されている更新時間がきているかどうかの判定
            now = time.time() # メンテ時はありえないほど大きい数字を入れる
            if(read_data[j]["latest_time"] + read_data[j]["update_time"] <= now):
                response =  requests.get(api_url + read_data[j]["name"])
                result = response.json()

                # data_jsonフォルダからラウンジapiの古い情報を取得
                with open('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + read_data[j]["name"] + ".ndjson") as f:
                    read_data2 = ndjson.load(f)
                

                old_info = read_data2[0]["mmrChanges"]
                new_info = result["mmrChanges"]
                
                # Placement（ラウンジを始めたばっかりの人）やシーズンが始まったばっかりの時に動く判定処理
                if len(new_info) == 1 or len(new_info) == 0:
                    
                    if read_data[j]["season_alert"] == 0:
                        embed=discord.Embed(title="データがありません！\n新しいユーザーであるか、もしくは新シーズンが始まりました！\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
                        if len(new_info) == 1:
                            # 更新された日付・時刻を格納→変換
                            date = dateutil.parser.parse(new_info[0]["time"]).astimezone(JST)
                            embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " JST", value="", inline=False)
                            embed.add_field(name="Now mmr:  " + str(new_info[0]["newMmr"]), value=" ", inline=True)
                        else:
                            embed.add_field(name="No data.", value=" ", inline=True)

                        channel_sent = client.get_channel(read_data[j]["channel"])
                        await channel_sent.send(embed=embed)

                        read_data[j]["season_alert"] = 1 
                    
                    # read_data2に最新の情報を書きこむ
                    os.remove('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + read_data[j]["name"] + ".ndjson")
                    with open('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + read_data[j]["name"] + ".ndjson", 'a') as f:
                        writer = ndjson.writer(f)
                        writer.writerow(result)

                    # 名前に変更があった場合、read_dataの名前を変更する
                    if result["name"] != read_data[j]["name"]:
                        read_data[j]["name"] = result["name"]
                    
                    # read_dataのlatest_timeを更新
                    read_data[j]["latest_time"] = time.time()
                    with open('./guild_json/' + os.path.split(files[i])[1], 'w') as f:
                        ndjson.dump(read_data, f)
                    
                    print("Placement（ラウンジを始めたばっかりの人）やシーズンが始まったばっかりの時に動く判定でcontinueしました")
                    
                    continue
                
                #print(read_data[j]["name"])
                #print(len(new_info))
                #print(len(old_info))
                #channel_sent = client.get_channel(1090113806174273606) # debug
                #await channel_sent.send(len(new_info)) # debug
                if len(old_info) == 0:
                    hozon = len(new_info) - (len(new_info) - 1) 
                else:
                    for k in range(0, len(new_info)):
                        if old_info[0]["changeId"] == new_info[k]["changeId"]:
                            hozon = k
                            break
                #print(hozon)
                if hozon == 0:
                    # read_data2に最新の情報を書きこむ
                    os.remove('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + read_data[j]["name"] + ".ndjson")
                    with open('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + read_data[j]["name"] + ".ndjson", 'a') as f:
                        writer = ndjson.writer(f)
                        writer.writerow(result)

                    # 名前に変更があった場合、read_dataの名前を変更する
                    if result["name"] != read_data[j]["name"]:
                        read_data[j]["name"] = result["name"]
                    
                    # read_dataのlatest_timeを更新
                    read_data[j]["latest_time"] = time.time()
                    with open('./guild_json/' + os.path.split(files[i])[1], 'w') as f:
                        ndjson.dump(read_data, f)
                    
                    print("hozon = 0の判定でcontinueしました")
                    continue
                
                for l in range(hozon-1,-1,-1):
                    #print(l)
                    # 更新された日付・時刻を格納→変換
                    date = dateutil.parser.parse(new_info[l]["time"]).astimezone(JST)

                    # ランクを判定する season8時点のランクを入れておく seasonが変わることに確認する必要あり
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

                    embed=discord.Embed(title="戦績が更新されました！\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
                    embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " JST", value="", inline=False)
                    embed.add_field(name="mmr:  " + str(new_info[l]["newMmr"]), value=" ", inline=True)
                    embed.add_field(name="+ / - :  " + mmrdelta, value=" ", inline=True)
                    embed.add_field(name="Now Rank:  " + rank, value=" ", inline=True)
                    embed.add_field(name="・詳細をサイトで見る", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=True)
                    embed.set_image(url="https://www.mk8dx-lounge.com/TableImage/" + str(new_info[l]["changeId"]) + ".png")
                    
                    # channel idを抽出する
                    #id = read_data[j]["channel"]
                    #id = id[2:]
                    #id = id[:-1]
                    
                    channel_sent = client.get_channel(read_data[j]["channel"])
                    await channel_sent.send(embed=embed)
                
                # read_data2に最新の情報を書きこむ
                os.remove('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + read_data[j]["name"] + ".ndjson")
                with open('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + result["name"] + ".ndjson", 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(result)
                
                # 名前に変更があった場合、read_dataの名前を変更する
                if result["name"] != read_data[j]["name"]:
                    read_data[j]["name"] = result["name"]
                
                # season_alertの初期化処理
                if len(new_info) > 1 and read_data[j]["season_alert"] == 1:
                    read_data[j]["season_alert"] = 0
                
                # read_dataのlatest_timeを更新
                read_data[j]["latest_time"] = time.time()

                with open('./guild_json/' + os.path.split(files[i])[1], 'w') as f:
                    ndjson.dump(read_data, f)
                
                print("表示し、更新する所までの処理を全て正常に通過しました")


#Bot commands
# /send_add
@tree.command(name="send_add",description="戦績を送信するプレイヤーを追加し、特定のチャンネルにそれを送信するようにします。")
async def send_add(interaction: discord.Interaction,lounge_name:str,channel:discord.TextChannel):
    await interaction.response.defer(ephemeral=True)

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

    response =  requests.get(api_url + lounge_name)
    
    #print(response.status_code)
    if response.status_code != 200:
        print("エラー！:このラウンジの名前は存在しません！")
        embed=discord.Embed(title="エラー！", description="このラウンジの名前は存在しません！", color=0xff0000)
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
        if(os.path.split(files[i])[1] == lounge_name + ".ndjson"):
            #print("一致しました！")
            judge = 1
            break
    
    if judge != 1:
        # print(interaction.guild.id)

        with open('./data_json/' + str(interaction.guild.id) + '/' + lounge_name + ".ndjson", 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(result)
    else:
        #file = str(interaction.guild.id) + ".ndjson"
        with open('./data_json/' + str(interaction.guild.id) + '/' + lounge_name + ".ndjson") as f:
                    read_data = ndjson.load(f)
        
        judge = 1
        for i in range(0, len(read_data)):
            if lounge_name == read_data[i]["name"]:
                judge = 0
                break
        
        if judge == 0:
            embed=discord.Embed(title="エラー！", description=":x:既に同じ名前の人が登録されています。:x:", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return
    
    # guild_jsonフォルダにサーバーidのフォルダを作成
    content = {
            "name" : lounge_name,
            "latest_time": time.time(),
            "update_time": update_time,
            "channel": channel.id,
            "season_alert": 0
    }

    with open('./guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
        writer = ndjson.writer(f)
        writer.writerow(content)

    print("登録しました!:" + lounge_name + "として入力された内容を保存しました。")
    embed=discord.Embed(title="登録しました!", description=lounge_name + "として入力された内容を保存しました。", color=0x00ff7f)
    await interaction.followup.send(embed=embed)

    #await interaction.response.send_message(text, ephemeral=False)

# /send_delete
@tree.command(name="send_delete",description="指定された戦績を送信するプレイヤーを削除します。")
async def send_delete(interaction: discord.Interaction,lounge_name:str):
    await interaction.response.defer(ephemeral=True)
    
    #print(lounge_name)

    response =  requests.get(api_url + lounge_name)
    
    #print(response.status_code)
    if response.status_code != 200:
        print("エラー！:このラウンジの名前は存在しません！")
        embed=discord.Embed(title="エラー！", description="このラウンジの名前は存在しません！", color=0xff0000)
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
        embed=discord.Embed(title="エラー!", description=":x:このサーバーのデータがありません。:x:", color=0xff0000)
        await interaction.followup.send(embed=embed)
        return
    
    # 指定のユーザーのndjsonファイルが存在しているかの確認
    files = glob.glob('./data_json/' + str(interaction.guild.id) + '/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == lounge_name + ".ndjson"):
            #print("一致しました！")
            judge = 1
            break
    
    if judge != 1:
        embed=discord.Embed(title="エラー!", description=":x:指定されたユーザーのデータがありません。:x:", color=0xff0000)
        await interaction.followup.send(embed=embed)
        return
    
    # data_jsonファルダにあるユーザーデータの削除
    os.remove('./data_json/' + str(interaction.guild.id) + '/' + lounge_name + ".ndjson")

    # data_jsonフォルダ内のサーバーフォルダの中身がなくなりそうな場合にフォルダを削除する
    if len(files) == 1:
        os.rmdir('./data_json/' + str(interaction.guild.id))
    
    # guild_jsonフォルダにある、サーバーidのndjsonフォルダから、ユーザーデータの削除
    with open('./guild_json/' + str(interaction.guild.id) + ".ndjson") as f:
        read_data = ndjson.load(f)
                
    if len(read_data) == 1:
        os.remove('./guild_json/' + str(interaction.guild.id) + ".ndjson")
    else:
        data_write = 0
        print(read_data)
        for i in range(0, len(read_data)):
            if lounge_name == read_data[i]["name"]:
                del read_data[i]
                #print(read_data)
                #data_write = 1
                break

        #if data_write == 1:
        os.remove('./guild_json/' + str(interaction.guild.id) + ".ndjson")

        for i in range(0, len(read_data)):
            with open('./guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
                writer = ndjson.writer(f)
                writer.writerow(read_data[i])
    
    print("削除成功！:" + lounge_name + "を削除しました。また利用する際には/send_addコマンドを使用して、追加してください。")
    embed=discord.Embed(title="削除成功！", description=lounge_name + "を削除しました。\nまた利用する際には/send_addコマンドを使用して、追加してください。", color=0x00ff7f)
    await interaction.followup.send(embed=embed)

    #await interaction.response.send_message(text, ephemeral=False)

# /send_list
@tree.command(name="send_list",description="戦績を送信するために登録されているプレイヤーを表示します。")
async def send_list(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)

    # 指定のユーザーのndjsonファイルが存在しているかの確認
    files = glob.glob('./guild_json/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
            #print("一致しました！")
            judge = 1
            break
    
    if judge != 1:
        embed=discord.Embed(title="エラー!", description=":x:このサーバーには登録されているプレイヤーがいません。:x:", color=0xff0000)
        await interaction.followup.send(embed=embed)
        return
     
    with open('./guild_json/' + str(interaction.guild.id) + ".ndjson") as f:
        read_data = ndjson.load(f)
    
    embed=discord.Embed(title="登録されているプレイヤー")
    
    for i in range(0, len(read_data)):
        embed.add_field(name=read_data[i]["name"], value="投稿先チャンネル：<#" + str(read_data[i]["channel"]) + ">", inline=False)

    await interaction.followup.send(embed=embed)

# /help
@tree.command(name="help",description="コマンドについての簡単な使い方を出します。")
async def help(interaction: discord.Interaction):
        embed=discord.Embed(title="Command list")
        embed.add_field(name="/send_add [ラウンジ名] [投稿チャンネル（「#○○○」の形）]", value="戦績を送信するプレイヤーを追加します。", inline=False)
        embed.add_field(name="/send_delete [ラウンジ名]", value="戦績を送信するプレイヤーの削除を行います。", inline=False)
        embed.add_field(name="/send_list", value="戦績を送信する登録があるプレイヤーの一覧を表示します。", inline=False)
        embed.add_field(name="/help", value="このBotのコマンドの簡単な使い方を出します。", inline=False)
        '''
        if interaction.guild.id == your_guild_id: # もしサーバー限定コマンドの実装があった場合の表記をした場合はここに書く
            embed.add_field(name="", value="", inline=False)
        '''
        await interaction.response.send_message(embed=embed,ephemeral=False)

client.run(os.environ['token'])
