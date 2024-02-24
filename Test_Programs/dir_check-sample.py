import os
import glob

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