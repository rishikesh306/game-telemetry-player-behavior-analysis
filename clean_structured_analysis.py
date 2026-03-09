# Required libraries for player analysis

import pyarrow.parquet as pq
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as mpimg

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

def load_data(folder_path="player_data/February_10"):

    files = os.listdir(folder_path)

    first_file = files[0]

    file_path = os.path.join(folder_path, first_file)

    print("Opening file:", first_file)

    table = pq.read_table(file_path)

    df = table.to_pandas()

    # convert event bytes → string
    df["event"] = df["event"].apply(
        lambda x: x.decode("utf-8") if isinstance(x, bytes) else x
    )

    
    return df
  
# -----------------------------------------------------
# APPLY FILTERS
# -----------------------------------------------------

def apply_filters(df, selected_map="AmbroseValley"):

    filtered_df = df.copy()

    # map filter
    filtered_df = filtered_df[filtered_df["map_id"] == selected_map]

    # match filter
    selected_match = filtered_df["match_id"].iloc[0]
    filtered_df = filtered_df[filtered_df["match_id"] == selected_match]

    return filtered_df


# -----------------------------------------------------
# APPLY TIMELINE
# -----------------------------------------------------

def apply_timeline(df, seconds=10):

    total_rows = len(df)
    ratio = seconds / 300
    cutoff = int(total_rows * ratio)

    return df.iloc[:cutoff]


# -----------------------------------------------------
# CONVERT WORLD COORDINATES → MINIMAP COORDINATES
# -----------------------------------------------------

def convert_coordinates(df):

    origin_x = -370
    origin_z = -473
    scale = 900
    map_size = 4320

    df["map_x"] = ((df["x"] - origin_x) / scale) * map_size
    df["map_y"] = (1 - ((df["z"] - origin_z) / scale)) * map_size

    return df

# -----------------------------------------------------
# SEPARATE GAME EVENTS
# -----------------------------------------------------

def separate_events(df):

    human_df = df[df["event"] == "Position"].sort_values("ts")
    bot_df = df[df["event"] == "BotPosition"].sort_values("ts")

    kill_df = df[df["event"] == "Kill"]
    death_df = df[df["event"] == "Killed"]

    botkill_df = df[df["event"] == "BotKill"]
    botdeath_df = df[df["event"] == "BotKilled"]

    loot_df = df[df["event"] == "Loot"]
    storm_df = df[df["event"] == "KilledByStorm"]

    return human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df

# -----------------------------------------------------
# PLOT PLAYER JOURNEY
# -----------------------------------------------------

def plot_journey(human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df):

    map_img = mpimg.imread("minimaps/AmbroseValley_Minimap.png")

    plt.figure(figsize=(10, 8))
    plt.imshow(map_img)

    plt.xlim(0,4320)
    plt.ylim(4320,0)

    # start & end points
    if len(human_df) > 0:
        plt.scatter(human_df["map_x"].iloc[0], human_df["map_y"].iloc[0],
                    color="green", s=100, label="Start")

        plt.scatter(human_df["map_x"].iloc[-1], human_df["map_y"].iloc[-1],
                    color="red", s=100, label="End")

    # movement lines
    plt.plot(human_df["map_x"], human_df["map_y"], linewidth=2, label="Human Movement")
    plt.plot(bot_df["map_x"], bot_df["map_y"], linewidth=2, color="orange", label="Bot Movement")

    # events
    plt.scatter(loot_df["map_x"], loot_df["map_y"], color="yellow", label="Loot")

    plt.scatter(kill_df["map_x"], kill_df["map_y"],
                color="green", marker="*", s=120, label="Kill")

    plt.scatter(death_df["map_x"], death_df["map_y"],
                color="red", marker="x", s=120, label="Death")

    plt.scatter(botkill_df["map_x"], botkill_df["map_y"],
                color="lime", marker="*", s=120, label="Bot Kill")

    plt.scatter(botdeath_df["map_x"], botdeath_df["map_y"],
                color="darkred", marker="x", s=120, label="Bot Death")

    plt.scatter(storm_df["map_x"], storm_df["map_y"],
                color="purple", marker="X", s=120, label="Storm Death")

    plt.xlabel("X Coordinate")
    plt.ylabel("Z Coordinate")
    plt.title("Player Journey with Game Events")

    plt.legend()
   

# -----------------------------------------------------
# PLOT HEATMAPS
# -----------------------------------------------------

def plot_heatmaps(human_df, kill_df, botkill_df, death_df, botdeath_df):

    map_img = mpimg.imread("minimaps/AmbroseValley_Minimap.png")

    # PLAYER TRAFFIC
    fig1, ax1 = plt.subplots(figsize=(6,5))
    ax1.imshow(map_img)
    ax1.set_xlim(0,4320)
    ax1.set_ylim(4320,0)
    if len(human_df) > 1:  # ← add pannu
        sns.kdeplot(x=human_df["map_x"], y=human_df["map_y"],
                    cmap="Reds", fill=True, thresh=0.05,
                    warn_singular=False, ax=ax1)
    ax1.set_title("Player Traffic")

    # KILL ZONES
    all_kills = pd.concat([kill_df, botkill_df])
    fig2, ax2 = plt.subplots(figsize=(6,5))
    ax2.imshow(map_img)
    ax2.set_xlim(0,4320)
    ax2.set_ylim(4320,0)
    if len(all_kills) > 1:  # ← add pannu
        sns.kdeplot(x=all_kills["map_x"], y=all_kills["map_y"],
                    cmap="Greens", fill=True, thresh=0.05,
                    warn_singular=False, ax=ax2)
    ax2.set_title("Kill Zones")

    # DEATH ZONES
    all_deaths = pd.concat([death_df, botdeath_df])
    fig3, ax3 = plt.subplots(figsize=(6,5))
    ax3.imshow(map_img)
    ax3.set_xlim(0,4320)
    ax3.set_ylim(4320,0)
    if len(all_deaths) > 1:  # ← add pannu
        sns.kdeplot(x=all_deaths["map_x"], y=all_deaths["map_y"],
                    cmap="Blues", fill=True, thresh=0.05,
                    warn_singular=False, ax=ax3)
    ax3.set_title("Death Zones")

    return fig1, fig2, fig3
   
# -----------------------------------------------------
# MAIN PIPELINE
# -----------------------------------------------------

def main():

    # 1 Load data
    df = load_data()

    # 2 Apply filters
    df = apply_filters(df)

    # 3 Apply timeline
    df = apply_timeline(df, seconds=10)

    # 4 Convert coordinates
    df = convert_coordinates(df)

    # 5 Separate events
    human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df = separate_events(df)

    # 6 Plot journey
    plot_journey(human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df)

    # 7 Plot heatmaps
    plot_heatmaps(human_df, kill_df, botkill_df, death_df, botdeath_df)


# run program
if __name__ == "__main__":
    main()
