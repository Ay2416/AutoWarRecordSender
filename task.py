# Discord bot import
import discord
import os
import glob
import sys
import math
import traceback
import ndjson
import time
import datetime
import dateutil.parser
import requests
import asyncio
import json

# My program import
# None

update_time =  30 # 更新間隔を設定（秒）
api_url = "https://www.mk8dx-lounge.com/api/player/details?name="
api_url_id = "https://www.mk8dx-lounge.com/api/player/details?id="
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
UTC = datetime.timezone(datetime.timedelta(hours=0), 'UTC')

class Task:
    async def send_message(self, bot):

        try:
            # guild_jsonのファイル一覧を取得
            files = glob.glob('./guild_json/' + '*.ndjson')
            
            # 戦績の更新があるかどうかを確認する処理
            for i in range(0, len(files)):
                #print("a")

                # 言語の確認
                read_data = await Task.read_ndjson('./language_json/' + os.path.split(files[i])[1])
                language = read_data[0]["language_mode"]

                # 処理対象のサーバーのデータを読み込む
                read_data = await Task.read_ndjson('./guild_json/' + os.path.split(files[i])[1])

                for j in range(0, len(read_data)):
                    #print("i")
                    # apiサーバー気休めのためのディレイをかける
                    await asyncio.sleep(1)

                    # 設定されている更新時間がきているかどうかの判定
                    now = time.time() # メンテ時はありえないほど小さい数字を入れる
                    if(read_data[j]["latest_time"] + update_time <= now):
                        
                        response =  requests.get(api_url_id + str(read_data[j]["playerId"]))
                        
                        try:
                            result = response.json()
                        except Exception:
                            # 主にラウンジシーズン切り替え時のメンテナンス時に発生すると思われる
                            print("requestsで返ってきた情報がjson形式ではないエラーでcontinueしました")
                            continue

                        #print(response.status_code)
                        if response.status_code != 200:
                            print("ラウンジのサーバーが落ちている可能性がある判定でcontinueしました")
                            continue

                        # data_jsonフォルダからラウンジapiの古い情報を取得
                        read_data2 = await Task.read_ndjson('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + 
                                                        "/" + str(read_data[j]["playerId"]) + ".ndjson")

                        print(str(read_data2[0]["playerId"]) + "の処理を開始します")

                        # データを参照しやすいようにmmrの情報のみを抽出
                        old_info = read_data2[0]["mmrChanges"]
                        new_info = result["mmrChanges"]
                        
                        # eventPlayedが0のとき = Placement（ラウンジを始めたばっかりの人）やシーズンが始まったばっかりの時に動く判定処理
                        if result["eventsPlayed"] == 0:
                            if len(new_info) == 0 and read_data[j]["season_alert"] == 0:
                                await Task.send_season_alert(bot, language, read_data[j]["channel"], result, new_info, "OFF")
                                read_data[j]["season_alert"] = 1
                            elif len(new_info) == 1 and read_data[j]["season_alert"] == 1:
                                await Task.send_season_alert(bot, language, read_data[j]["channel"], result, new_info, "ON")
                                read_data[j]["season_alert"] = 2
                            
                            # read_data2に最新の情報を書きこむ
                            os.remove('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(read_data[j]["playerId"]) + ".ndjson")
                            await Task.write_ndjson('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(result["playerId"]) + ".ndjson", result)

                            '''
                            # 名前に変更があった場合、read_dataの名前を変更する
                            if result["name"] != read_data[j]["name"]:
                                read_data[j]["name"] = result["name"]
                            '''
                            
                            # read_dataのlatest_timeを更新
                            read_data[j]["latest_time"] = time.time()

                            os.remove('./guild_json/' + os.path.split(files[i])[1])
                            
                            await Task.update_ndjson('./guild_json/' + os.path.split(files[i])[1], read_data)
                            
                            print("Placement（ラウンジを始めたばっかりの人）やシーズンが始まったばっかりの時に動く判定でcontinueしました")
                            
                            continue
                        
                        #print(read_data[j]["name"])
                        #print(len(new_info))
                        #print(len(old_info))

                        hozon = 0 # 戦績結果の更新をする回数を保存する用
                        counta = 0
                        changeId_none = 0
                        reference_num = 0
                        while counta < len(new_info):
                            # Placementだった場合を考えて（PlacementがreasonになっているものにはchangeIdが存在しない）
                            # ワンチャンこの下のif文いらないかも？
                            #if new_info[k]["reason"] == "Placement":
                            #    break

                            if old_info[reference_num]["reason"] == "Placement":
                                break
                            
                            if len(new_info) - 1 == counta:
                                counta = 0
                                reference_num += 1
                                continue

                            if old_info[reference_num]["changeId"] == new_info[counta]["changeId"]:
                                hozon = counta
                                changeId_none = 1
                                break
                            else:
                                pass

                            counta += 1

                        # changeIdが存在しなくてPlacementだった場合
                        # changeIdが存在しなくてそのseasonをある程度遊んでいる場合
                        if changeId_none == 0:
                            hozon = len(new_info) - ( len(new_info) - 1 )


                        #print(hozon)
                        if hozon == 0:
                            # read_data2に最新の情報を書きこむ
                            os.remove('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(read_data[j]["playerId"]) + ".ndjson")
                            await Task.write_ndjson('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(result["playerId"]) + ".ndjson", result)

                            '''
                            # 名前に変更があった場合、read_dataの名前を変更する
                            if result["name"] != read_data[j]["name"]:
                                read_data[j]["name"] = result["name"]
                            '''
                            
                            # read_dataのlatest_timeを更新
                            read_data[j]["latest_time"] = time.time()

                            os.remove('./guild_json/' + os.path.split(files[i])[1])
                            
                            await Task.update_ndjson('./guild_json/' + os.path.split(files[i])[1], read_data)
                            print("更新がない判定でcontinueしました")
                            continue
                        
                        mention_count1 = 0
                        for k in range(hozon-1,-1,-1):
                            #print(l)

                            # ランクを判定する season9時点のランクを入れておく seasonが変わることに確認する必要あり
                            rank = await Task.rank_judge(new_info[k]["newMmr"])

                            # mmrDeltaに+の数値であれば+を付ける判定
                            if new_info[k]["mmrDelta"] > 0:
                                mmrdelta = "+" + str(new_info[k]["mmrDelta"])
                            else:
                                mmrdelta = str(new_info[k]["mmrDelta"])

                            if read_data[j]["normal_mention"] != "null" and mention_count1 == 0:
                                mention_result = await Task.mention_check(bot, language, read_data[j]["channel"], read_data[j]["normal_mention"], 
                                                                    int(os.path.splitext(os.path.basename(files[i]))[0]))
                            
                                if mention_result != "success":
                                    continue

                                mention_count1 = 1

                            # どういう理由でmmrが増減したかを確認する処理
                            if new_info[k]["reason"] != "Table":
                                send_result = await Task.send_other_message(bot, language, read_data[j]["channel"], mmrdelta, rank, result, new_info[k]["time"],
                                                                            new_info[k]["reason"], new_info[k]["newMmr"])
                            else:
                                send_result = await Task.send_record_message(bot, language, read_data[j]["channel"], mmrdelta, rank, result, new_info[k]["time"], 
                                                                        new_info[k]["newMmr"], new_info[k]["numTeams"], new_info[k]["changeId"])
                            
                            if send_result == "success":
                                pass
                            
                            # channel idを抽出する
                            #id = read_data[j]["channel"]
                            #id = id[2:]
                            #id = id[:-1]

                            # ランクアップ通知の処理
                            # 今シーズン5戦以上していたら処理をする
                            if result["eventsPlayed"] >= 5 and read_data[j]["rankup_notification"] == "on":
                                now_rank = await Task.rank_judge(new_info[k]["newMmr"])
                                old_rank = await Task.rank_judge(new_info[k+1]["newMmr"])

                                now_mmr_floor = math.floor(new_info[k]["newMmr"] / 1000)
                                old_mmr_floor = math.floor(new_info[k+1]["newMmr"] / 1000)
                                peak_mmr_floor = math.floor(result["maxMmr"] / 1000)

                                peak_mmr = result["maxMmr"]
                                now_mmr = new_info[k]["newMmr"]
                                
                                if int(now_mmr_floor - old_mmr_floor) == 1:

                                    rankup_judge = 0
                                    if peak_mmr - now_mmr != 0:
                                        print("a")
                                        # 帰ってきた通知
                                        # メンションを希望の場合
                                        if read_data[j]["rankup_mention"] != "null" and mention_count1 == 0:
                                            print("mention!")
                                            await Task.mention_check(bot, language, read_data[j]["channel"], read_data[j]["rankup_mention"], 
                                                            int(os.path.splitext(os.path.basename(files[i]))[0]))
                                            
                                            mention_count1 = 1
                                            
                                        # メッセージ送信
                                        await Task.send_rankup_notification(bot, language, read_data[j]["channel"], result, old_rank, now_rank, "other")

                                    else:
                                        print("b")
                                        for l in range(len(new_info)-2, -1, -1):
                                            if peak_mmr_floor - int(math.floor(new_info[l]["newMmr"] / 1000)) == 0:
                                                rankup_judge = 1
                                                break
                                    
                                        # メンションを希望の場合
                                        if read_data[j]["rankup_mention"] != "null" and mention_count1 == 0:
                                            print("mention!")
                                            await Task.mention_check(bot, language, read_data[j]["channel"], read_data[j]["rankup_mention"], 
                                                            int(os.path.splitext(os.path.basename(files[i]))[0]))
                                            
                                            mention_count1 = 1

                                        if rankup_judge == 0:
                                            print("c")
                                            # 初めての通知
                                            await Task.send_rankup_notification(bot, language, read_data[j]["channel"], result, old_rank, now_rank, "first")
                                        else:
                                            print("d")
                                            # 帰ってきた通知
                                            await Task.send_rankup_notification(bot, language, read_data[j]["channel"], result, old_rank, now_rank, "other")

                        # read_data2に最新の情報を書きこむ
                        os.remove('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(read_data[j]["playerId"]) + ".ndjson")
                        
                        await Task.write_ndjson('./data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + "/" + str(result["playerId"]) + ".ndjson", result)

                        
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
                        
                        await Task.update_ndjson('./guild_json/' + os.path.split(files[i])[1], read_data)
                        
                        print("表示し、更新する所までの処理を全て正常に通過しました")
                
                print("No." + str(i + 1) + " " + os.path.splitext(os.path.basename(files[i]))[0] + "のサーバーの処理が終了しました")
        except Exception as e:
            #print(traceback.format_exc())
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

            print("タスクエラーが発生しました。")
    
    # mmrをもとにどのランク帯にいるかを返す
    async def rank_judge(rank_num):
        rank = ''

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
        #    old_rank = "Placement"

        return rank

    # ndjsonの後ろにデータを追加する = データ追加
    async def write_ndjson(file_path, write_data):
        with open(file_path, 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(write_data)

    # ndjsonのデータを更新する = データを更新
    async def update_ndjson(file_path, write_data):
        for i in range(0, len(write_data)):
            with open(file_path, 'a') as f:
                writer = ndjson.writer(f)
                writer.writerow(write_data[i])

    # ndjsonファイルを読み込む = データを読み込む
    async def read_ndjson(file_path):
        with open(file_path) as f:
            read_data = ndjson.load(f)
        
        return read_data

    # メンションを送る処理と、エラーが発生した場合の処理
    async def mention_check(bot, language, channel_id, user_id, guild_id):

        channel_sent = bot.get_channel(channel_id)

        try:
            await channel_sent.send("<@" + user_id + ">")
        except Exception as e:
            try:
                guild = bot.get_guild(guild_id)
                user = await bot.fetch_user(int(user_id))
                
                if language == "ja":
                    embed=discord.Embed(title="送信エラー",description= guild.name + 
                                        "のサーバーでメッセージを送信することができませんでした。" + 
                                        "\nこの通知がしばらく続く場合は、このBotを使用しているサーバーで/send add, /send deleteコマンドで再登録を行うか、" + 
                                        "\nサポートサーバーへ連絡を入れてください。\n(このBotを使用しているサーバーで/supportを打つことで招待リンクを見れます。)", 
                                        color=0x00008b)
                elif language == "en":
                    embed=discord.Embed(title="Send Error", description="A message could not be sent on " + guild.name + 
                                        "server.\nIf this notification persists for some time, \nplease re-register using the /send add, " + 
                                        "/send delete commands or\ncontact the support server.\n(You can see the invite link by hitting " + 
                                        "/supprt on the server using this bot.)", color=0x00008b)
                
                await user.send(embed=embed)

                print("normal_mentionかrankup_mentionエラーでcontinueしました。")
                return "error"
            
            except Exception:
                print("normal_mentionかrankup_mentionエラーを送信できませんでした。continueします。")
                return "error"
        else:
            return "success"

    # 新規ユーザーと、新シーズンの際に送るメッセージの処理
    async def send_season_alert(bot, language, channel_id, result, new_info, mmr_view):
        if mmr_view == "ON":
            if language == "ja":
                embed=discord.Embed(title="シーズン" + str(result["season"]) + "へようこそ！\n\n" + result["name"] 
                                    + " Season" + str(result["season"]) + " War Record", color=0x00008b)
            elif language == "en":
                embed=discord.Embed(title="Welcome to Season " + str(result["season"]) +"\n\n" + result["name"] 
                                    + " Season" + str(result["season"]) + " War Record", color=0x00008b)
            
            # 更新された日付・時刻を格納→変換
            if language == "ja":
                date = dateutil.parser.parse(new_info[0]["time"]).astimezone(JST)
                embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " JST", value="", inline=False)
            elif language == "en":
                date = dateutil.parser.parse(new_info[0]["time"]).astimezone(UTC)
                embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " UTC", value="", inline=False)  
            
            embed.add_field(name="Now mmr:  " + str(new_info[0]["newMmr"]), value=" ", inline=True)
            
        else:
            if language == "ja":
                embed=discord.Embed(title="データがありません！\n新しいユーザーであるか、もしくは新シーズンが始まります！\n\n" + result["name"], color=0x00008b)
            elif language == "en":
                embed=discord.Embed(title="No data!\nNew User or New Season!\n\n" + result["name"], color=0x00008b)
            
            embed.add_field(name="No data.", value=" ", inline=True)
            
        if language == "ja":
            embed.add_field(name="・詳細をサイトで見る", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=False)
        elif language == "en":
            embed.add_field(name="・View detail", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=False)
        
        channel_sent = bot.get_channel(channel_id)
        await channel_sent.send(embed=embed)
    
    # Penalty Strike Bonus StrikeDelete TableDeleteの際に送るメッセージの処理
    async def send_other_message(bot, language, channel_id, mmrdelta, rank, result, time, reason, newmmr):
        if reason == "Penalty" or reason == "Strike":
            #ストライクまたはペナルティの場合
            if language == "ja":
                embed=discord.Embed(title="ストライクまたはペナルティを受けました💦\n\n" + result["name"] + " Season" + str(result["season"]) + 
                                    " War Record", color=0x00008b)
            elif language == "en":
                embed=discord.Embed(title="Strike or penalty received💦\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
        else:
            # ボーナス、ストライクの削除、テーブルの削除の場合
            if language == "ja":
                embed=discord.Embed(title="MMRが変更されています！\n\n" + result["name"] + " Season" + str(result["season"]) + 
                                    " War Record", color=0x00008b)
            elif language == "en":
                embed=discord.Embed(title="MMR has been changed!\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)

        # 更新された日付・時刻を格納→変換
        if language == "ja":
            date = dateutil.parser.parse(time).astimezone(JST)
            embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " JST", value="", inline=False)
        elif language == "en":
            date = dateutil.parser.parse(time).astimezone(UTC)
            embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " UTC", value="", inline=False)    

        embed.add_field(name="Reason:  " + reason, value="", inline=False)        
        embed.add_field(name="mmr:  " + str(newmmr), value="", inline=True)
        embed.add_field(name="+ / - :  " + mmrdelta, value="", inline=True)
        embed.add_field(name="Now Rank:  " + rank, value="", inline=False)
        
        if language == "ja":
            embed.add_field(name="・詳細をサイトで見る", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=False)
        elif language == "en":
            embed.add_field(name="・View detail", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=False)
        
        if reason == "Penalty" or reason == "Strike":
            if language == "ja":
                embed.add_field(name="・もし本人の場合はサイトで確認し、本当にストライクまたはペナルティがついていた場合、何故なのかルールを確認してみましょう。", 
                                value="https://www.mk8dx-lounge.com/Rules", inline=False)
            elif language == "en":
                embed.add_field(name="・If it is the person, check the site and if it is indeed a strike or penalty, check the rules to see why.", 
                                value="https://www.mk8dx-lounge.com/Rules", inline=False)

        try:
            channel_sent = bot.get_channel(channel_id)
            await channel_sent.send(embed=embed)
        
            print(reason + "の通知を送りました")

            return "success"
        except Exception:
            print(reason + "の通知を送信できませんでした。passします。")
            
            return "pass"

    # 戦績を送る際のメッセージの処理
    async def send_record_message(bot, language, channel_id, mmrdelta, rank, result, time, newmmr, numteams, changeid):
        if language == "ja":
            embed=discord.Embed(title="戦績が更新されました！\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
        elif language == "en":
            embed=discord.Embed(title="Update War Record！\n\n" + result["name"] + " Season" + str(result["season"]) + " War Record", color=0x00008b)
        
        # 更新された日付・時刻を格納→変換
        if language == "ja":
            date = dateutil.parser.parse(time).astimezone(JST)
            embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " JST", value="", inline=False)
        elif language == "en":
            date = dateutil.parser.parse(time).astimezone(UTC)
            embed.add_field(name= date.strftime("%Y/%m/%d %H:%M:%S") + " UTC", value="", inline=False)    
        
        embed.add_field(name="mmr:  " + str(newmmr) + " (" + rank + ")", value="", inline=True)
        embed.add_field(name="+ / - :  " + mmrdelta, value="", inline=True)
        embed.add_field(name="Team num: " + str(numteams), value="", inline=False)
        
        if language == "ja":
            embed.add_field(name="・詳細をサイトで見る", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=True)
        elif language == "en":
            embed.add_field(name="・View detail", value="https://www.mk8dx-lounge.com/PlayerDetails/" + str(result["playerId"]), inline=True)
        embed.set_image(url="https://www.mk8dx-lounge.com/TableImage/" + str(changeid) + ".png")

        try:
            channel_sent = bot.get_channel(channel_id)
            await channel_sent.send(embed=embed)
        
            print("戦績の通知を送りました")

            return "success"
        except Exception:
            print("戦績の通知を送信できませんでした。passします。")
            
            return "pass"
    
    # ランクアップ通知を送る際のメッセージの処理
    async def send_rankup_notification(bot, language, channel_id, result, old_rank, now_rank, view_mode):
        if view_mode == "first":
            if language == "ja":
                embed=discord.Embed(title="下記のユーザーのランクが上がりました！\n\n", color=0x00008b)
                embed.add_field(name=":tada:おめでとうございます！:tada:\n" + result["name"] + " Season" + str(result["season"]) + "\n" + old_rank + " :arrow_upper_right: " + now_rank, value=" ", inline=True)
            elif language == "en":
                embed=discord.Embed(title="The following users have been Rank up!\n\n", color=0x00008b)
                embed.add_field(name=":tada:congratulations!:tada:\n" + result["name"] + " Season" + str(result["season"]) + "\n" + old_rank + " :arrow_upper_right: " + now_rank, value=" ", inline=True)
        else:
            if language == "ja":
                embed=discord.Embed(title="下記のユーザーのランクが上がりました！\n\n", color=0x00008b)
                embed.add_field(name=":tada:おかえりなさい！:tada:\n" + result["name"] + " Season" + str(result["season"]) + "\n" + old_rank +":arrow_upper_right: " + now_rank, value=" ", inline=True)
            elif language == "en":
                embed=discord.Embed(title="The following users have been Rank up!\n\n", color=0x00008b)
                embed.add_field(name=":tada:Come back!:tada:\n" + result["name"] + " Season" + str(result["season"]) + "\n" + old_rank +":arrow_upper_right: " + now_rank, value=" ", inline=True)

        channel_sent = bot.get_channel(channel_id)
        await channel_sent.send(embed=embed)