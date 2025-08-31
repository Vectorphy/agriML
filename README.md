# AI-Powered Agricultural Monitoring Platform (Proof-of-Concept)

This project is a proof-of-concept (PoC) Streamlit application designed for the analysis of agricultural hyperspectral and multispectral data. It provides a user-friendly interface to load remote sensing data, perform various analyses, and visualize the results on an interactive map.

## Features

*   **Modular Backend**: Analysis functions are separated from the UI for clarity and maintainability.
*   **Multiple Analysis Types**:
    *   **Vegetation Indices**: Calculate and visualize common VIs like NDVI, SAVI, NDWI, and NDRE.
    *   **Crop Classification**: Train a Random Forest classifier on labeled data to generate a crop type map.
    *   **Temporal Analysis**: Simulate and analyze a time-series of NDVI data to detect anomalies in crop health over a growing season.
*   **Interactive GUI**:
    *   Built with Streamlit for a user-friendly experience.
    *   Interactive map powered by Folium for visualizing geospatial data.
    *   Location search to easily navigate the map.
    *   Dynamically updated results panel.

## Project Structure

```
.
├── analysis_backend/
│   ├── __init__.py
│   ├── classification.py   # Logic for crop classification
│   ├── data_processing.py  # Data loading functions
│   ├── indices.py          # Vegetation Index calculations
│   └── temporal.py         # Temporal analysis and simulation
├── app.py                  # Main Streamlit application script
├── data/
│   ├── SalinasA.mat        # Default dataset for VI and Classification
│   └── SalinasA_gt.mat     # Ground truth for SalinasA
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Setup and Installation

1.  **Clone the repository** (or ensure all files are in the same directory).

2.  **Install system dependencies**: On Debian/Ubuntu, some Python packages require the GEOS library.
    ```bash
    sudo apt-get update && sudo apt-get install -y libgeos-dev
    ```

3.  **Create a Python virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

Once the setup is complete, you can run the application by executing the `main.py` script:

```bash
python main.py
```

This will launch the Streamlit application in your web browser.

The application should open in your web browser automatically.

## Overview of Analysis Phases

### Phase 1 & 2: Spectral Analysis & Classification

This application uses the **Salinas-A** hyperspectral dataset as a default for demonstrating vegetation index calculation and crop classification.

*   **Vegetation Indices**: Select one of the four implemented VIs (NDVI, SAVI, NDWI, NDRE) from the sidebar. The application will compute the index and display a heatmap overlay on the map, along with a plot of the resulting data.
*   **Crop Classification**: The app trains a Random Forest model on the Salinas-A ground truth labels. It displays the resulting classification map and key performance metrics, including Overall Accuracy, Precision, Recall, and a confusion matrix.

### Phase 3: Temporal Analysis (Simulated)

Due to challenges with accessing a suitable public time-series dataset without authentication, this feature is demonstrated using **simulated data**.

*   **Simulation**: The application uses the Salinas-A dataset to generate a realistic, 13-step NDVI time-series that mimics a typical growing season.
*   **Anomaly Detection**: A simple statistical model is used to detect anomalies. It calculates a 3-point rolling average of the NDVI values and flags any point that deviates by more than a set number of standard deviations.
*   **Visualization**: The results are shown as a line chart of the NDVI trend over time, with any detected anomalies clearly highlighted in red.

#### Future Work: Advanced Anomaly Detection

The current statistical model serves as a baseline. For a more robust and predictive system, this model could be replaced with a more advanced network, such as a **Long Short-Term Memory (LSTM) recurrent neural network**. An LSTM would be better suited to learn the complex temporal patterns of crop growth and could be used not only for anomaly detection but also for predictive forecasting of crop yields or health issues.
