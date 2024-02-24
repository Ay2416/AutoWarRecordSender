# discord import
import os
import glob
import time
import requests
import math
import ndjson
import discord
#import traceback

# my program import

delay_time = 15 # /send_add,/send_deleteの使える間隔の設定（秒）
player_api = "https://www.mk8dx-lounge.com/api/player/details?id="
player_api_id = "https://www.mk8dx-lounge.com/api/player?discordId="

class ContextMenu:
    async def add_send_program(self, interaction, member):

        #await interaction.response.defer()

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
                
                await interaction.response.send_message(embed=embed)
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

        content = {
            "member" : member.id
        }

        with open('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson', 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(content)

        # 番号を入力するためのウィンドウを表示する
        await interaction.response.send_modal(answer_input())

# モーダルウィンドウ用のクラス
class answer_input(discord.ui.Modal, title='次の項目を選択してください。 / Select setting ON or OFF.'):

    normal_mention_a = discord.ui.TextInput(
        label='通常通知メンション / Normal notification mention',
        placeholder='ON = 1, OFF = 2',
    )

    rankup_notification_a = discord.ui.TextInput(
        label='ランクアップ通知 / Rankup notification',
        placeholder='ON = 1, OFF = 2',
    )

    rankup_mention_a = discord.ui.TextInput(
        label='ランクアップ通知メンション / Rankup notification mention',
        placeholder='ON = 1, OFF = 2',
    )

    async def on_submit(self, interaction: discord.Interaction):

        await interaction.response.defer()

        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        # 入力されたものが数字であるかどうか
        try:
            answer1 = int(self.normal_mention_a.value)
            answer2 = int(self.rankup_notification_a.value)
            answer3 = int(self.rankup_mention_a.value)
            #print(answer)
        except Exception as e:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:入力されたものが数字ではありません。\nもう一度コマンドを実行しなおしてください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:What was entered is not a number. \nPlease execute the command again.:x:", color=0xff0000)
            #await interaction.message.delete()
            os.remove('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson')
            await interaction.followup.send(embed=embed)
            return
        
        # 入力された数字が範囲内にあるか
        #print(count)
        if answer1 < 1 or answer1 > 2:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:入力された数字が有効ではありません。\nもう一度コマンドを実行しなおしてください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:The number entered is not valid. \nPlease execute the command again.:x:", color=0xff0000)

            #await interaction.message.delete()
            os.remove('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson')
            await interaction.followup.send(embed=embed)
            return

        if answer2 < 1 or answer2 > 2:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:入力された数字が有効ではありません。\nもう一度コマンドを実行しなおしてください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:The number entered is not valid. \nPlease execute the command again.:x:", color=0xff0000)

            #await interaction.message.delete()
            os.remove('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson')
            await interaction.followup.send(embed=embed)
            return

        if answer3 < 1 or answer3 > 2:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:入力された数字が有効ではありません。\nもう一度コマンドを実行しなおしてください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:The number entered is not valid. \nPlease execute the command again.:x:", color=0xff0000)

            #await interaction.message.delete()
            os.remove('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson')
            await interaction.followup.send(embed=embed)
            return

        # リーダーボードからデータを取得
        # 最初にID情報を取得
        with open('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson') as f:
            read_data = ndjson.load(f)

        response = requests.get(player_api_id + str(read_data[0]["member"]))
        result = response.json()
        
        if response.status_code == 404:
            if language == "ja":
                embed=discord.Embed(title="エラー!", description=":x:このユーザーは存在しない可能性があります。\n入力した内容を確認してください。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:This user may not exist. \nPlease check the information you have entered.:x:", color=0xff0000)
            
            os.remove('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson')
            await interaction.followup.send(embed=embed)

            print("184このユーザーは存在しない可能性があります。入力した内容を確認してください。")
            return
        
        if response.status_code != 200:
            if language == "ja":
                embed=discord.Embed(title="エラー!", description=":x:リーダーボードが落ちている可能性があります。\nしばらくしてからお試しください。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:The leaderboard may be down. \nPlease try again after a while.:x:", color=0xff0000)
            
            os.remove('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson')
            await interaction.followup.send(embed=embed)

            print("ラウンジのサーバーが落ちている可能性があります。")
            return
        
        # プレイヤー情報を取得
        response = requests.get(player_api + str(result["id"]))
        result = response.json()
        
        if response.status_code == 404:
            if language == "ja":
                embed=discord.Embed(title="エラー!", description=":x:このユーザーは存在しない可能性があります。\n入力した内容を確認してください。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:This user may not exist. \nPlease check the information you have entered.:x:", color=0xff0000)
            
            os.remove('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson')
            await interaction.followup.send(embed=embed)

            print("213このユーザーは存在しない可能性があります。入力した内容を確認してください。")
            return
        
        if response.status_code != 200:
            if language == "ja":
                embed=discord.Embed(title="エラー!", description=":x:リーダーボードが落ちている可能性があります。\nしばらくしてからお試しください。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:The leaderboard may be down. \nPlease try again after a while.:x:", color=0xff0000)
            
            os.remove('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson')
            await interaction.followup.send(embed=embed)

            print("ラウンジのサーバーが落ちている可能性があります。")
            return

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
                
                os.remove('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson')
                await interaction.followup.send(embed=embed)
                return
            
        # メンション用の処理
        normal_user = ""
        if answer1 == 1:
            normal_user = str(interaction.user.id)
        else:
            normal_user = "null"
        
        rankup_user = ""
        if answer3 == 1:
            rankup_user = str(interaction.user.id)
        else:
            rankup_user = "null"
        
        # ランクアップ通知用の処理
        rankup_notification = ""
        if answer2 == 1:
            rankup_notification = "on"
        else:
            rankup_notification = "off"

        # guild_jsonフォルダにサーバーidのフォルダを作成
        content = {
                "playerId" : result["playerId"],
                "latest_time": time.time(),
                "channel": interaction.channel.id,
                "season_alert": 0,
                "normal_mention": normal_user,
                "rankup_notification" : rankup_notification,
                "rankup_mention" : rankup_user
        }

        with open('./guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(content)

        print("登録しました!:" + result["name"] + "として入力された内容を保存しました。")
        if language == "ja":
            embed=discord.Embed(title="登録しました!", description=result["name"] + "さんを追加しました。", color=0x00ff7f)
        elif language == "en":
            embed=discord.Embed(title="Registered!", description=result["name"] + " added.", color=0x00ff7f)        
        os.remove('./data_json/ContextMenuTemp_' + str(interaction.user.id) + '.ndjson')
        await interaction.followup.send(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:

        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        if language == "ja":
            await interaction.followup.send('エラーが発生しました。', ephemeral=False)
        else:
            await interaction.followup.send('An error has occurred.' , ephemeral=False)
            
        #traceback.print_exception(type(error), error, error.__traceback__)