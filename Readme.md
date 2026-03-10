# Player Behavior Analysis – Game Telemetry  

## Methodology Prototype & Scalable Dashboard


## Project Overview

This project analyzes player behavior using game telemetry data stored in **Parquet files**.

### Objective

- Player movement patterns  
- Combat behavior  
- Gameplay events  
- Spatial activity distribution  

The analysis converts raw telemetry logs into meaningful player behavior insights using structured data processing and visualization techniques.

---

## Development Strategy

The full dataset contains multiple folders of telemetry files collected across several days.

Instead of directly processing the entire dataset, the development was done in stages to ensure clarity and correctness.

---

## Phase 1 – Methodology Development (Single File Prototype)

To build a reliable pipeline, the analysis started with:

> Only the first telemetry file from the first folder.

This was done intentionally to deeply understand the structure before scaling.

### Tasks Performed

- Studied the schema and structure of telemetry data  
- Identified and decoded gameplay event types  
- Handled timestamp parsing and filtering  
- Converted world coordinates into minimap pixel coordinates  
- Separated gameplay events:
  - Movement  
  - Kills  
  - Deaths  
  - Loot  
  - Storm eliminations  
- Built and validated initial visualization logic  

This phase helped establish a clear and reusable methodology for large-scale processing.

---

## Phase 2 – Visualization & Validation

Using the processed data from the single file, the following visualizations were created:

### Player Journey Map

- Displays player movement on the game minimap  
- Marks events such as kills, deaths, loot interactions, and storm eliminations  

### Player Traffic Heatmap

- Shows areas where players spend the most time  

### Kill Zone Heatmap

- Highlights combat-intensive regions  

### Death Zone Heatmap

- Identifies high-risk areas on the map  

This validated both coordinate transformation accuracy and event segmentation logic.

---

## Live Demo – Single File Prototype

🔗 **Single File GitHub Repository**  
https://github.com/rishikesh306/game-telemetry-player-behavior-analysis

🔗 **Single File Streamlit App**  
https://game-telemetry-player-behavior-analysis-hh9raoxarlxpankv769iav.streamlit.app/

---

# Full Project – Scalable Telemetry Dashboard

After validating the methodology using one telemetry file, the same pipeline was extended to process the complete dataset.

### Full Implementation Includes

- 5 days of telemetry data  
- 1,243 files  
- ~89,000 event rows  
- Match filtering  
- Map selection  
- Timeline-based visualization  
- Interactive heatmaps and journey tracking  

---

## Full Project Links

🔗 **Full GitHub Repository**  
https://github.com/rishikesh306/LILA-_Black_Telemetry_dashboard

🔗 **Full Streamlit Dashboard**  
https://lila-blacktelemetrydashboard-miqwtowrayof47w7wdrqou.streamlit.app/

---

# Deployment Notes (Important)

The full dashboard is deployed using the free version of Streamlit Cloud.

Since the dataset is relatively large (~89,000 rows across 1,243 files), some infrastructure-related limitations may occur.

---

## 1. App Sleep / Initial Loading Delay

If the dashboard is opened after some inactivity:

- It may take time to load  
- It may appear temporarily unresponsive  

This happens because the free cloud environment automatically goes to sleep when not in use.

Additionally, loading large telemetry datasets requires significant RAM usage.

If the app does not respond:

    Wait for the initial load
    OR  
    Refresh the page

If the issue persists:

- Clone/download the repository

- Run locally using:
    - streamlit run app_all_days.py

Running locally does not produce these issues, as local system RAM resources are available.

---
## 2. Timeline Filter Usage Recommendation

While using the timeline slider:

- Adjust time in small increments (5–10 seconds)

- Avoid jumping across large time ranges at once

- Large jumps increase memory usage in the free cloud environment and may cause a temporary crash.

This issue does not occur when running locally.

---
## 3. Occasional Match Loading Issue

- Due to the large number of files and event rows:

- A selected match may occasionally fail to load

- The visualization may not render properly

- If This Happens

      Refresh the page 
      OR
      Select another match
      OR
      Switch to a different day

This is related to cloud resource limitations, not the processing logic.

---
## Why These Notes Are Mentioned

As a student developer, I believe it is important to clearly communicate deployment constraints along with technical implementation.

The analytical pipeline works as expected.
The mentioned limitations are related to free-tier cloud infrastructure.

---
## Tools & Technologies

- Python

- Pandas

- PyArrow

- Matplotlib

- Seaborn

- Streamlit

---
## Conclusion

This project demonstrates:

- Structured data understanding

- Telemetry event processing

- Coordinate transformation logic

- Scalable pipeline design

- Interactive dashboard deployment

---
The single-file prototype demonstrates clarity of methodology.
The full implementation demonstrates scalability and practical deployment experience.

---
