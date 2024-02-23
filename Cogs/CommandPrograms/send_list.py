# Discord bot import
import discord
import os
from dotenv import load_dotenv
import glob
import ndjson
import asyncio

# My program import


class list:
    async def list_info(self, interaction):
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
        
        normal_mention_setting = " "
        cut = 25
        for i in range(0, len(read_data)):
            if read_data[i]["normal_mention"] != "null":
                normal_mention_setting = "on"
            else:
                normal_mention_setting = "off"
            
            if read_data[i]["rankup_mention"] != "null":
                rankup_mention_setting = "on"
            else:
                rankup_mention_setting = "off"

            with open('./data_json/' + str(interaction.guild.id) + '/' + str(read_data[i]["playerId"]) + '.ndjson') as f:
                read_data2 = ndjson.load(f)
            
            if language == "ja":
                embed.add_field(name=read_data2[0]["name"], value="投稿先チャンネル：<#" + str(read_data[i]["channel"]) + ">\n通常メンション：" + normal_mention_setting + "\nランクアップ通知：" + read_data[i]["rankup_notification"] + "\nランクアップメンション：" + rankup_mention_setting, inline=False)
            elif language == "en":
                embed.add_field(name=read_data2[0]["name"], value="Send Channel: <#" + str(read_data[i]["channel"]) + ">\nNormal mention: " + normal_mention_setting+ "\nRankup notification: " + read_data[i]["rankup_notification"] + "\nRankup mention: " + rankup_mention_setting, inline=False)
            
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