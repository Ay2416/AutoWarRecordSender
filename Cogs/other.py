# Discord bot import
import discord
from discord import app_commands
from discord.ext import commands
import os
import requests
import ndjson
import glob

# My program import

delay_time = 15 # /send_add,/send_deleteの使える間隔の設定（秒）
player_api_name = "https://www.mk8dx-lounge.com/api/player?name="
player_api_id = "https://www.mk8dx-lounge.com/api/player?discordId="

class other(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # /language
    @app_commands.command(name="language",description="言語を変更します。（jaまたはen） / Change language. (ja or en)")
    @app_commands.guild_only()
    @app_commands.choices(language=[discord.app_commands.Choice(name="ja",value="ja"),discord.app_commands.Choice(name="en",value="en")])
    async def language_command(self, interaction: discord.Interaction,language:str):
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
    @app_commands.command(name="help",description="コマンドについての簡単な使い方を出します。 / How to use command and Command list.")
    @app_commands.guild_only()
    async def help_command(self, interaction: discord.Interaction):
        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        #Discord上にヘルプを表示
        if language == "ja":
            embed=discord.Embed(title="コマンドリスト")
            embed.add_field(name="/send add\nlounge_name:[ラウンジ名]\nchannel:[投稿チャンネル（「#○○○」の形）]\nnormal_mention[戦績通知のメンションの有無（on/off）]\nrankup_notification:[ランクアップ通知の有無（on/off）]\nrankup_mention:[ランクアップ通知のメンションの有無（on/off）]", value="戦績を送信するプレイヤーを追加します。\nまた、メンション設定はオンにした場合、コマンドを入力したプレイヤーにメンションが行くように設定されます。\nそして、ランクアップ通知の項目の入力は必須ではありません。\n※コマンドクールタイムが " + str(delay_time) + " 秒あります。（/send add, /send deleteコマンド共通）", inline=False)
            embed.add_field(name="/send delete lounge_name:[ラウンジ名]", value="戦績を送信するプレイヤーの削除を行います。\n※コマンドクールタイムが " + str(delay_time) + " 秒あります。（/send add, /send delteコマンド共通）", inline=False)
            embed.add_field(name="/send list", value="戦績を送信する登録があるプレイヤーの一覧を表示します。", inline=False)
            embed.add_field(name="/fc lounge_name:[ラウンジ名]", value="プレイヤーのフレンドコードを表示します。\n※ラウンジ名は必須ではありません。", inline=False)
            embed.add_field(name="/mmr lounge_name:[ラウンジ名]", value="プレイヤーの現在のmmrと今のランクを表示します。\n※ラウンジ名は必須ではありません。", inline=False)
            embed.add_field(name="/mkc lounge_name:[ラウンジ名]", value="プレイヤーのマリオカートセントラルのプロフィールページを表示します。\n※ラウンジ名は必須ではありません。", inline=False)
            embed.add_field(name="/language language:[言語の選択（ja/en）]", value="このBotのコマンドの言語を変更します。", inline=False)
            embed.add_field(name="/help", value="このBotのコマンドの簡単な使い方を出します。", inline=False)
        elif language == "en":
            embed=discord.Embed(title="Command list")
            embed.add_field(name="/send add\nlounge_name:[Lounge name]\nchannel:[Send Channel ([#○○○])]\nnormal_mention[War record mention setting(on/off)]\nrankup_notification:[Send rankup notification setting (on/off)]\nrankup_mention:[Rankup notification setting (on/off)]", value="The War Record send player add.\nIn addition, the Mention setting, when turned on, is set so that the ments go to the player who entered the command.\nAnd the entry of the rank-up notification field is not required.\n※Command cool time" + str(delay_time) + " seconds. (/send add, /send delete command common)", inline=False)
            embed.add_field(name="/send delete lounge_name:[Lounge name]", value="The War Record send player delete.\n※Command cool time" + str(delay_time) + " seconds. (/send add, /send delete command common)", inline=False)
            embed.add_field(name="/send list", value="The War Record send player list view.", inline=False)
            embed.add_field(name="/fc lounge_name:[Lounge name]", value="Display player friend code.\n*Lounge name is not required.", inline=False)
            embed.add_field(name="/mmr lounge_name:[Lounge name]", value="Displays the player current mmr and current rank.\n*Lounge name is not required.", inline=False)
            embed.add_field(name="/mkc lounge_name:[Lounge name]", value="Displays the player Mario Kart Central profile page.\n*Lounge name is not required.", inline=False)
            embed.add_field(name="/language language:[language setting（ja/en）]", value="Change default language.", inline=False)
            embed.add_field(name="/help", value="How to use command and Command list.", inline=False)

        '''
        if interaction.guild.id == your_guild_id: # もしサーバー限定コマンドの実装があった場合の表記をした場合はここに書く
            embed.add_field(name="", value="", inline=False)
        '''
        await interaction.response.send_message(embed=embed,ephemeral=False)

    # /fc
    @app_commands.command(name="fc",description="ユーザーのフレンドコードを表示します。 / User switch friend code display.")
    @app_commands.guild_only()
    async def fc_command(self, interaction: discord.Interaction,name:str=None):
        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        # もし名前の表記があれば
        if name != None:
            response = requests.get(player_api_name + name)
            result = response.json()
        else:
            response = requests.get(player_api_id + str(interaction.user.id))
            result = response.json()
        
        if response.status_code == 404:
            if language == "ja":
                embed=discord.Embed(title="エラー!", description=":x:このユーザーは存在しない可能性があります。\n入力した内容を確認してください。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:This user may not exist. \nPlease check the information you have entered.:x:", color=0xff0000)
            
            await interaction.response.send_message(embed=embed)

            print("このユーザーは存在しない可能性があります。入力した内容を確認してください。")
            return
        
        if response.status_code != 200:
            if language == "ja":
                embed=discord.Embed(title="エラー!", description=":x:リーダーボードが落ちている可能性があります。\nしばらくしてからお試しください。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:The leaderboard may be down. \nPlease try again after a while.:x:", color=0xff0000)
            
            await interaction.response.send_message(embed=embed)

            print("ラウンジのサーバーが落ちている可能性があります。")
            return

        if language == "ja":
            embed=discord.Embed(title="フレンドコード (" + result["name"]  +  ")", description=result["switchFc"], color=0x00ff7f)
        elif language == "en":
            embed=discord.Embed(title="Friend code (" + result["name"]  +  ")", description=result["switchFc"], color=0x00ff7f)
        
        await interaction.response.send_message(embed=embed)
            
    # /mmr
    @app_commands.command(name="mmr",description="150ccラウンジの現在のmmrを表示します。 / 150cc Lounge now mmr display.")
    @app_commands.guild_only()
    async def mmr_command(self, interaction: discord.Interaction,name:str=None):
        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        # もし名前の表記があれば
        if name != None:
            response = requests.get(player_api_name + name)
            result = response.json()
        else:
            response = requests.get(player_api_id + str(interaction.user.id))
            result = response.json()
        
        if response.status_code == 404:
            if language == "ja":
                embed=discord.Embed(title="エラー!", description=":x:このユーザーは存在しない可能性があります。\n入力した内容を確認してください。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:This user may not exist. \nPlease check the information you have entered.:x:", color=0xff0000)
            
            await interaction.response.send_message(embed=embed)

            print("このユーザーは存在しない可能性があります。入力した内容を確認してください。")
            return
        
        if response.status_code != 200:
            if language == "ja":
                embed=discord.Embed(title="エラー!", description=":x:リーダーボードが落ちている可能性があります。\nしばらくしてからお試しください。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:The leaderboard may be down. \nPlease try again after a while.:x:", color=0xff0000)
            
            await interaction.response.send_message(embed=embed)

            print("ラウンジのサーバーが落ちている可能性があります。")
            return

        # ランクを判定する season9時点のランクを入れておく seasonが変わることに確認する必要あり
        rank_num = result["mmr"]

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
        if language == "ja":
            embed=discord.Embed(title="現在のmmr (" + result["name"]  +  ")", description=str(result["mmr"]) + " (" + rank + ")", color=0x00ff7f)
        elif language == "en":
            embed=discord.Embed(title="Now mmr (" + result["name"]  +  ")", description=str(result["mmr"]) + " (" + rank + ")", color=0x00ff7f)

        await interaction.response.send_message(embed=embed)

    # /mkc
    @app_commands.command(name="mkc",description="マリオカートセントラルのページを表示します。 / Mario Kart Central Page display.")
    @app_commands.guild_only()
    async def mkc_command(self, interaction: discord.Interaction,name:str=None):
        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        # もし名前の表記があれば
        if name != None:
            response = requests.get(player_api_name + name)
            result = response.json()
        else:
            response = requests.get(player_api_id + str(interaction.user.id))
            result = response.json()
        
        if response.status_code == 404:
            if language == "ja":
                embed=discord.Embed(title="エラー!", description=":x:このユーザーは存在しない可能性があります。\n入力した内容を確認してください。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:This user may not exist. \nPlease check the information you have entered.:x:", color=0xff0000)
            
            await interaction.response.send_message(embed=embed)

            print("このユーザーは存在しない可能性があります。入力した内容を確認してください。")
            return
        
        if response.status_code != 200:
            if language == "ja":
                embed=discord.Embed(title="エラー!", description=":x:リーダーボードが落ちている可能性があります。\nしばらくしてからお試しください。:x:", color=0xff0000)
            elif language == "en":
                embed=discord.Embed(title="Error!", description=":x:The leaderboard may be down. \nPlease try again after a while.:x:", color=0xff0000)
            
            await interaction.response.send_message(embed=embed)

            print("ラウンジのサーバーが落ちている可能性があります。")
            return

        if language == "ja":
            embed=discord.Embed(title="マリオカートセントラルページ (" + result["name"]  +  ")", description="https://www.mariokartcentral.com/mkc/registry/players/" + str(result["registryId"]), color=0x00ff7f)
        elif language == "en":
            embed=discord.Embed(title="Mario Kart Central Page (" + result["name"]  +  ")", description="https://www.mariokartcentral.com/mkc/registry/players/" + str(result["registryId"]), color=0x00ff7f)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(other(bot))