import ndjson
import glob
import os

# guild_jsonのファイル一覧を取得
files = glob.glob('./guild_json/' + '*.ndjson')

# 戦績の更新があるかどうかを確認する処理
for i in range(0, len(files)):
    #print("a")
    file_name = os.path.split(files[i])[1]

    with open('./guild_json/' + os.path.split(files[i])[1]) as f:
            read_data = ndjson.load(f)
    
    os.remove('./guild_json/' + os.path.split(files[i])[1])

    for j in range(0, len(read_data)):

        content = {
                "playerId" : read_data[j]["playerId"],
                "latest_time": read_data[j]["latest_time"],
                "channel": read_data[j]["channel"],
                "season_alert": 2,
                "normal_mention": read_data[j]["normal_mention"],
                "rankup_notification" : read_data[j]["rankup_notification"],
                "rankup_mention" : read_data[j]["rankup_mention"]
        }
        
        with open('./guild_json/' + str(file_name), 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(content)
        
        print("updated.")
    
    print(os.path.splitext(os.path.basename(files[i]))[0] + "のサーバーのファイルの処理が終了しました")
