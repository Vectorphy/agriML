# Author: Jules
#
# © 2025 Jules
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import time
import os

# Import backend functions
from analysis_backend.data_processing import load_salinas_data
from analysis_backend.indices import calculate_ndvi, calculate_savi, calculate_ndwi, calculate_ndre
from analysis_backend.classification import classify_pixels
from analysis_backend.temporal import simulate_ndvi_time_series, detect_anomalies, plot_temporal_analysis

# --- Page Configuration ---
st.set_page_config(
    page_title="Agri-PoC Platform",
    page_icon="🌿",
    layout="wide"
)

# --- Caching ---
# Cache the data loading to avoid reloading on every interaction
@st.cache_data
def cached_load_data(data_path, gt_path=None):
    """A cached wrapper for the backend data loading function."""
    return load_salinas_data(data_path, gt_path)

@st.cache_data
def run_classification_analysis(_data_cube, _ground_truth):
    with st.spinner('Training Random Forest and classifying pixels... This may take a moment.'):
        class_map, metrics = classify_pixels(_data_cube, _ground_truth)
    return class_map, metrics

@st.cache_data
def run_temporal_analysis(_data_cube, _ground_truth):
     with st.spinner('Simulating time series and detecting anomalies...'):
        ts_df = simulate_ndvi_time_series(_data_cube, _ground_truth)
        ts_with_anomaly = ts_df.copy()
        # Artificially create an anomaly for demonstration
        anomaly_index = 6
        ts_with_anomaly.loc[anomaly_index, 'ndvi'] *= 0.4
        analysis_df = detect_anomalies(ts_with_anomaly, std_dev_threshold=1.0)
        fig = plot_temporal_analysis(ts_with_anomaly, analysis_df)
     return fig, analysis_df

# --- Main App ---
st.title("🌿 AI-Powered Agricultural Monitoring Platform")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Controls")

    st.subheader("1. Load Data")
    st.info("This PoC uses the Salinas-A dataset by default. The uploader is for demonstration.")

    data_file = st.file_uploader("Upload Hyperspectral Data (.mat)", type=["mat"])
    gt_file = st.file_uploader("Upload Ground Truth Data (.mat)", type=["mat"])

    # This logic is for a future implementation where uploaded files are used.
    # For now, we are forcing the use of the default dataset.
    # if data_file is not None:
    #     st.session_state['data_path'] = f"/tmp/{data_file.name}"
    #     with open(st.session_state['data_path'], "wb") as f:
    #         f.write(data_file.getbuffer())
    # if gt_file is not None:
    #     st.session_state['gt_path'] = f"/tmp/{gt_file.name}"
    #     with open(st.session_state['gt_path'], "wb") as f:
    #         f.write(gt_file.getbuffer())


    st.subheader("2. Select Analysis")
    analysis_type = st.selectbox(
        "Choose Analysis Type",
        ["Vegetation Indices", "Crop Classification", "Temporal Analysis"]
    )

    # Conditional UI for VI
    if analysis_type == "Vegetation Indices":
        vi_selection = st.selectbox(
            "Choose Vegetation Index",
            ["NDVI", "SAVI", "NDWI", "NDRE"]
        )

    if st.button("Run Analysis", type="primary"):
        st.session_state['run_analysis'] = True
    else:
        st.session_state['run_analysis'] = False


# --- Main Panel ---
# Initialize session state for map center
if 'map_center' not in st.session_state:
    st.session_state['map_center'] = [36.310, -121.645] # Default to Salinas, CA

# Two-column layout
col1, col2 = st.columns([0.4, 0.6])

with col1:
    st.header("Map & Location")

    # Location Search
    search_term = st.text_input("Search for a city (e.g., 'Nagpur, India')")
    if st.button("Search"):
        try:
            geolocator = Nominatim(user_agent="agri-poc-app")
            location = geolocator.geocode(search_term)
            if location:
                st.session_state['map_center'] = [location.latitude, location.longitude]
                st.success(f"Map centered on {location.address}")
            else:
                st.error("Location not found.")
        except Exception as e:
            st.error(f"Geocoding failed: {e}")

    # Create and display the map
    m = folium.Map(location=st.session_state['map_center'], zoom_start=12)

    if st.session_state.get('overlay_map') is not None:
        folium.raster_layers.ImageOverlay(
            image=st.session_state['overlay_map'],
            bounds=st.session_state['overlay_bounds'],
            opacity=0.7,
            name='Analysis Overlay'
        ).add_to(m)
        folium.LayerControl().add_to(m)
        st.info("Analysis overlay added to the map. Note: Geolocation is a hardcoded placeholder for the Salinas dataset.")

    st_folium(m, width='100%', height=400)


with col2:
    st.header("Analysis Results")
    if not st.session_state.get('run_analysis'):
        st.info("Load data and click 'Run Analysis' to see results.")

    if st.session_state.get('run_analysis'):
        # For this PoC, we always use the default dataset.
        default_data_path = 'data/SalinasA.mat'
        default_gt_path = 'data/SalinasA_gt.mat'

        # Check if default files exist
        if not os.path.exists(default_data_path) or not os.path.exists(default_gt_path):
            st.error(f"Default data files not found in the 'data/' directory. Please ensure SalinasA.mat and SalinasA_gt.mat are present.")
        else:
            data_cube, ground_truth = cached_load_data(default_data_path, default_gt_path)

            if data_cube is None:
                st.error("Data could not be loaded. Please check the file or logs.")
            else:
                # --- VEGETATION INDICES ---
                if analysis_type == "Vegetation Indices":
                    st.subheader(f"{vi_selection} Results")
                    index_calculators = {"NDVI": calculate_ndvi, "SAVI": calculate_savi, "NDWI": calculate_ndwi, "NDRE": calculate_ndre}

                    with st.spinner(f'Calculating {vi_selection}...'):
                        index_map = index_calculators[vi_selection](data_cube)

                    display_map = (index_map - np.min(index_map)) / (np.max(index_map) - np.min(index_map))
                    st.session_state['overlay_map'] = display_map
                    st.session_state['overlay_bounds'] = [[36.30, -121.655], [36.32, -121.635]]

                    fig, ax = plt.subplots(); im = ax.imshow(index_map, cmap='viridis'); fig.colorbar(im, ax=ax); ax.set_title(f"{vi_selection} Map"); ax.axis('off'); st.pyplot(fig)

                # --- CROP CLASSIFICATION ---
                elif analysis_type == "Crop Classification":
                    st.subheader("Crop Classification Results")
                    if ground_truth is None:
                        st.error("Ground truth data is required for Crop Classification.")
                    else:
                        class_map, metrics = run_classification_analysis(data_cube, ground_truth)
                        display_map = class_map.astype(float) / np.max(class_map)
                        st.session_state['overlay_map'] = display_map
                        st.session_state['overlay_bounds'] = [[36.30, -121.655], [36.32, -121.635]]

                        st.metric("Overall Accuracy", f"{metrics['overall_accuracy']:.4f}")
                        st.metric("Avg. Precision", f"{metrics['precision']:.4f}")
                        st.metric("Avg. Recall", f"{metrics['recall']:.4f}")

                        fig, ax = plt.subplots(); im = ax.imshow(metrics['confusion_matrix'], cmap='Blues'); ax.set_title("Confusion Matrix"); ax.set_xlabel("Predicted"); ax.set_ylabel("Actual"); fig.colorbar(im, ax=ax); st.pyplot(fig)

                # --- TEMPORAL ANALYSIS ---
                elif analysis_type == "Temporal Analysis":
                    st.subheader("Temporal Analysis Results")
                    if ground_truth is None:
                        st.error("Ground truth data is required for Temporal Analysis simulation.")
                    else:
                        fig, analysis_df = run_temporal_analysis(data_cube, ground_truth)
                        st.session_state['overlay_map'] = None
                        st.pyplot(fig)
                        st.write("Anomaly Detection Details:"); st.dataframe(analysis_df)
