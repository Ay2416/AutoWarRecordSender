import os
import ndjson
import math

# 必要なのは　今のMMR、1個前のMMR、PeakMMR

with open('./test.ndjson') as f:
    read_data = ndjson.load(f)

# 変数宣言
now_mmr = 6000
old_mmr = 5000
peak_mmr = 7000

#now_mmr = int(read_data[0]["mmrChanges"][0]["newMmr"])
#old_mmr = int(read_data[0]["mmrChanges"][1]["newMmr"])
#peak_mmr = int(read_data[0]["maxMmr"]

now_mmr_floor = math.floor(now_mmr / 1000)
old_mmr_floor = math.floor(old_mmr / 1000)
peak_mmr_floor = math.floor(peak_mmr / 1000)

# 今のランクナンバーと1個前のランクナンバーの差を出して1であること
if now_mmr - old_mmr == 1:
    print("1です！")