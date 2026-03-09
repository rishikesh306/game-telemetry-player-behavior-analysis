# Player Behavior Analysis – Game Telemetry

## Project Goal

This project analyzes player behavior using game telemetry data stored in **Parquet files**.
The objective is to understand **player movement, combat patterns, and gameplay events** through data visualization and heatmaps.

---

## Current Development Approach

The dataset contains multiple folders of telemetry data.
To ensure a clean and reliable pipeline, the analysis is being developed in stages.

### Step 1 – Methodology Development

The **first folder** was used to design and validate the entire processing pipeline.

From this folder, **only the first telemetry file** was processed to:

* Understand the structure of the data
* Decode event types
* Handle timestamps and filtering
* Convert world coordinates to minimap coordinates
* Separate gameplay events (movement, kills, deaths, loot, etc.)
* Build visualization logic

This step helped establish a **clear methodology for the full analysis pipeline**.

---

### Step 2 – Visualization & Insights

Using the processed data, the following visualizations were created:

* **Player Journey Map**

  * Tracks player movement on the game minimap
  * Marks events like kills, deaths, loot, and storm eliminations

* **Player Traffic Heatmap**

  * Shows areas where players spend the most time

* **Kill Zone Heatmap**

  * Highlights combat-heavy regions

* **Death Zone Heatmap**

  * Identifies dangerous locations on the map

---

### Step 3 – Scalable Processing (Next Phase)

After validating the methodology using the first file, the **same pipeline will be applied to the remaining folders** in the dataset.

This will allow large-scale analysis of player behavior across multiple matches.

---

## Tools & Technologies

* **Python**
* **Pandas**
* **PyArrow**
* **Matplotlib**
* **Seaborn**
* **Streamlit** (for interactive dashboard)

---

## Future Improvements

* Process all telemetry folders automatically
* Build an interactive **Streamlit dashboard**
* Add timeline filters to analyze gameplay over time
* Compare player vs bot interactions
* Identify strategic hotspots on the map

---

## Outcome

This project demonstrates how **game telemetry data can be transformed into meaningful player behavior insights** using data engineering and visualization techniques.
