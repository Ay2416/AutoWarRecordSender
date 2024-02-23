# Discord bot import
import discord
import os
import glob
import ndjson
import time
import requests
import math

# My program import


delay_time = 15 # /send_add,/send_deleteの使える間隔の設定（秒）
api_url = "https://www.mk8dx-lounge.com/api/player/details?name="

class add:
    async def add_info(self, interaction, lounge_name, channel, normal_mention, rankup_notification, rankup_mention):
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

        '''
        if normal_mention == "on" or normal_mention == "off":
            print("成功！:メンションの設定通過！")
        else:
            print("エラー！:コマンドのメンションの設定が間違っています！ご確認ください。")
            if language == "ja":
                embed=discord.Embed(title="エラー！", description="コマンドのメンションの指定が間違っています！\nご確認ください。", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description="Command mention setting error!\nCheck typing keyword. ([on] or [off])", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return
        '''
            
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
        normal_user = ""
        if normal_mention == "on":
            normal_user = str(interaction.user.id)
        else:
            normal_user = "null"
        
        rankup_user = ""
        if rankup_mention == "on":
            rankup_user = str(interaction.user.id)
        else:
            rankup_user = "null"
        
        # guild_jsonフォルダにサーバーidのフォルダを作成
        content = {
                "playerId" : result["playerId"],
                "latest_time": time.time(),
                "channel": channel.id,
                "season_alert": 0,
                "normal_mention": normal_user,
                "rankup_notification" : rankup_notification,
                "rankup_mention" : rankup_user
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