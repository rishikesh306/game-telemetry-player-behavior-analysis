import pyarrow.parquet as pq  # For opening our dataset file since it is in parquet file format
import os  # It helps us to done file operation through command unlike manually
import pandas as pd # To convert arrow table to data frame to analyze the data's

folder_path = "player_data/February_10"

files = os.listdir(folder_path) # It will list all files in february_10 folder

first_file = files[0]  # first file access pannum since 0'th index

file_path = os.path.join(folder_path, first_file) # connecting first file path with folder path

print("Opening this file:", first_file) # It indicates that we opening the right file

table = pq.read_table(file_path) # parquet data's are stored in table format using pyarrow

# print(table) # print and viewing parquet data's in tabular format 

df = table.to_pandas() # transform arrow table to data frame

# convert event column data's from byte datatype to string datatype
df["event"] = df["event"].apply(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x) 

# timestamp convert
df["ts"] = pd.to_datetime(df["ts"], errors="coerce") # coerce prevent from crashing by adding Nat(Not a time) for invalid data

print("\nFirst 10 rows of data:\n")  # prints first 10 data rows
print(df.head(10))

# -------------------------------------------------------------------------------------------------------------------------------------
# filter section
filtered_df = df.copy()

selected_map = "AmbroseValley" # map filter
filtered_df = filtered_df[filtered_df["map_id"] == selected_map]
selected_match = filtered_df["match_id"].iloc[0] # match filter
filtered_df = filtered_df[filtered_df["match_id"] == selected_match]

df = filtered_df

# ---------------------------------------------------------------------------------------------------------------------------------------

# TIMELINE FILTER

time_limit = df["ts"].min() + pd.Timedelta(seconds=10)
df = df[df["ts"] <= time_limit]

# visualization part

import matplotlib.pyplot as plt
import seaborn as sns

# basic info
print("Total rows:", len(df))
print("Unique players:", df["user_id"].nunique())

print("\nEvent distribution:")
print(df["event"].value_counts())

# map coordinate convertion

origin_x = -370
origin_z = -473
scale = 900
map_size =  4320

df["map_x"] = ((df["x"] - origin_x) / scale) * map_size
df["map_y"] = (1 - ((df["z"] - origin_z) / scale)) * map_size
# -----------------------------------------------------------------------------------------------------------------------

# filter and separate events 

human_df = df[df["event"] == "Position"].sort_values("ts")
bot_df = df[df["event"] == "BotPosition"].sort_values("ts")

kill_df = df[df["event"] == "Kill"]
death_df = df[df["event"] == "Killed"]
botkill_df = df[df["event"] == "BotKill"]
botdeath_df = df[df["event"] == "BotKilled"]
loot_df = df[df["event"] == "Loot"]
storm_df = df[df["event"] == "KilledByStorm"]
# -----------------------------------------------------------------------------------------------------------------------------
# minimap visualization

import matplotlib.image as mpimg

# load map image
map_img = mpimg.imread("minimaps/AmbroseValley_Minimap.png")
print(map_img.shape)  # height, width, channels
plt.figure(figsize=(8,6))

plt.imshow(map_img)

plt.xlim(0,4320)
plt.ylim(4320,0) #map coordinate range

# -------------------------------------------------------------------------------------------------------------------------

# start & end
plt.scatter(human_df["map_x"].iloc[0], human_df["map_y"].iloc[0], color="green", s=100, label="Start")
plt.scatter(human_df["map_x"].iloc[-1], human_df["map_y"].iloc[-1], color="red", s=100, label="End")

# movement
plt.plot(human_df["map_x"], human_df["map_y"], linewidth=2, label="Human Movement")
plt.plot(bot_df["map_x"], bot_df["map_y"], linewidth=2, color="orange", label="Bot Movement")

# events
plt.scatter(loot_df["map_x"], loot_df["map_y"], color="yellow", marker="o", label="Loot")
plt.scatter(kill_df["map_x"], kill_df["map_y"], color="green", marker="*", s=120, label="Kill")
plt.scatter(death_df["map_x"], death_df["map_y"], color="red", marker="x", s=120, label="Death")
plt.scatter(botkill_df["map_x"], botkill_df["map_y"], color="lime", marker="*", s=120, label="Bot Kill")
plt.scatter(botdeath_df["map_x"], botdeath_df["map_y"], color="darkred", marker="x", s=120, label="Bot Death")
plt.scatter(storm_df["map_x"], storm_df["map_y"], color="purple", marker="X", s=120, label="Storm Death")

plt.xlabel("X Coordinate")
plt.ylabel("Z Coordinate")
plt.title("Player Journey with Game Events")

plt.legend()
plt.show()

# ----------------------------------------------------------------------------------------------------------------------------------------
# Heatmap visualization

# -------------------------------
# High Traffic Heatmap
# -------------------------------



plt.imshow(map_img)
plt.xlim(0,4320)
plt.ylim(4320,0)
         
sns.kdeplot(
    x=human_df["map_x"],
    y=human_df["map_y"],
    cmap="Reds",
    fill=True,
    thresh=0.05
)

plt.title("High Traffic Zones (Player Movement Density)")
plt.xlabel("X Coordinate")
plt.ylabel("Z Coordinate")

plt.show()

# -------------------------------
# Kill Zone Heatmap
# -------------------------------
all_kills = pd.concat([kill_df, botkill_df])

# plt.figure(figsize=(8,6))

plt.imshow(map_img)
plt.xlim(0,4320)
plt.ylim(4320,0)
         

sns.kdeplot(
    x=all_kills["map_x"],
    y=all_kills["map_y"],
    cmap="Greens",
    fill=True,
    thresh=0.05
)

plt.title("Kill Zones (Combat Hotspots)")
plt.xlabel("X Coordinate")
plt.ylabel("Z Coordinate")

plt.show()

# -------------------------------
# Death Zone Heatmap
# -------------------------------

all_deaths = pd.concat([death_df, botdeath_df])
# plt.figure(figsize=(8,6))
plt.imshow(map_img)
plt.xlim(0,4320)
plt.ylim(4320,0)
         

sns.kdeplot(
    x=all_deaths["map_x"],
    y=all_deaths["map_y"],
    cmap="Blues",
    fill=True,
    thresh=0.05
)

plt.title("Death Zones")
plt.xlabel("X Coordinate")
plt.ylabel("Z Coordinate")

plt.show()

# --------------------------------------------------------------------------------------------------------------------

