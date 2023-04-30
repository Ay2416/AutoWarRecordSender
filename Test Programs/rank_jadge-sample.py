# ※season8時点のもの
rank = input("You typing MK8DK 150cc Lounge mmr:")

rank_num = int(rank)

if rank_num >= 17000:
    jadge = "Grandmaster"
elif rank_num >= 16000:
    jadge = "Master"
elif rank_num >= 15000:
    jadge = "Diamond 2"
elif rank_num >= 14000:
    jadge = "Diamond 1"
elif rank_num >= 13000:
    jadge = "Ruby 2"
elif rank_num >= 12000:
    jadge = "Ruby 1"
elif rank_num >= 11000:
    jadge = "Sapphire 2"
elif rank_num >= 10000:
    jadge = "Sapphire 1"
elif rank_num >= 9000:
    jadge = "Platinum 2"
elif rank_num >= 8000:
    jadge = "Platinum 1"
elif rank_num >= 7000:
    jadge = "Gold 2"
elif rank_num >= 6000:
    jadge = "Gold 1"
elif rank_num >= 5000:
    jadge = "Silver 2"
elif rank_num >= 4000:
    jadge = "Silver 1"
elif rank_num >= 3000:
    jadge = "Bronze 2"
elif rank_num >= 2000:
    jadge = "Bronse 1"
elif rank_num >= 1000:
    jadge = "Iron 2"
elif rank_num >= 0:
    jadge = "Iron 1"
else:
    jadge = "Placement"

print(jadge)