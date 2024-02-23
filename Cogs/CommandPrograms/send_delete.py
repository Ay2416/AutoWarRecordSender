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

class delete:
    async def delete_info(self, interaction, lounge_name):

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
        
        print("削除成功！:" + lounge_name + "を削除しました。また利用する際には/send addコマンドを使用して、追加してください。")
        if language == "ja":
            embed=discord.Embed(title="削除成功！", description=lounge_name + "さんを削除しました。\nまた利用する際には/send addコマンドを使用して、追加してください。", color=0x00ff7f)
        elif language == "en":
            embed=discord.Embed(title="Deleted!", description=lounge_name + " deleted。\nWhen using it again, please use the /send add command to add it.", color=0x00ff7f)
        await interaction.followup.send(embed=embed)
        #await interaction.response.send_message(text, ephemeral=False)