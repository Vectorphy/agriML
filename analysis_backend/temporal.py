import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .data_processing import load_salinas_data
from .indices import calculate_ndvi

def simulate_ndvi_time_series(data_cube, ground_truth, field_class=1, num_steps=13):
    """
    Simulates a plausible NDVI time series for a selected crop field.

    Args:
        data_cube (np.ndarray): The hyperspectral data cube.
        ground_truth (np.ndarray): The ground truth map.
        field_class (int): The class ID of the fields to use for the simulation.
        num_steps (int): The number of time steps to simulate.

    Returns:
        pd.DataFrame: A DataFrame with 'date' and 'ndvi' columns.
    """
    # Find pixels belonging to the specified class
    field_pixels = np.where(ground_truth == field_class)
    if len(field_pixels[0]) == 0:
        print(f"No pixels found for class {field_class}. Using class 1 instead.")
        field_pixels = np.where(ground_truth == 1)
        if len(field_pixels[0]) == 0:
            raise ValueError("Could not find any labeled pixels to simulate time series.")


    # Calculate the base NDVI for these pixels
    base_ndvi = calculate_ndvi(data_cube)
    avg_base_ndvi = np.mean(base_ndvi[field_pixels])

    # Create a plausible seasonal curve (like a parabola)
    x = np.linspace(-1, 1, num_steps)
    # A downward-opening parabola starting and ending low, peaking in the middle
    seasonal_curve = -0.8 * (x**2) + 1

    # Scale the curve to a realistic NDVI range
    min_ndvi = avg_base_ndvi * 0.5  # Starts at 50% of base
    max_ndvi = avg_base_ndvi * 1.8  # Peaks at 180% of base
    scaled_curve = min_ndvi + (seasonal_curve * (max_ndvi - min_ndvi))

    # Add some random noise
    noise = np.random.normal(0, 0.02, num_steps)
    final_ndvi_series = np.clip(scaled_curve + noise, 0, 1) # Clip to valid NDVI range

    # Create a DataFrame
    dates = pd.to_datetime(pd.date_range(start='2023-01-01', periods=num_steps, freq='14D'))
    df = pd.DataFrame({'date': dates, 'ndvi': final_ndvi_series})

    return df

def detect_anomalies(time_series_df, window=3, std_dev_threshold=2.0):
    """
    Detects anomalies in a time series using a rolling mean.

    Args:
        time_series_df (pd.DataFrame): DataFrame with 'date' and 'ndvi' columns.
        window (int): The window size for the rolling mean.
        std_dev_threshold (float): The number of standard deviations to flag an anomaly.

    Returns:
        pd.DataFrame: The input DataFrame with added 'is_anomaly' boolean column.
    """
    df = time_series_df.copy()
    df['rolling_mean'] = df['ndvi'].rolling(window=window, center=True, min_periods=1).mean()
    df['rolling_std'] = df['ndvi'].rolling(window=window, center=True, min_periods=1).std()

    # Define anomaly condition
    df['is_anomaly'] = np.abs(df['ndvi'] - df['rolling_mean']) > (df['rolling_std'] * std_dev_threshold)

    # Handle NaNs in rolling_std for the first/last elements
    df['is_anomaly'] = df['is_anomaly'].fillna(False)

    return df

def plot_temporal_analysis(df, anomalies_df):
    """
    Generates a plot of the NDVI time series with anomalies highlighted.

    Args:
        df (pd.DataFrame): The original time series data.
        anomalies_df (pd.DataFrame): The DataFrame with anomaly detection results.

    Returns:
        matplotlib.figure.Figure: The plot figure.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the main time series
    ax.plot(df['date'], df['ndvi'], 'b-o', label='NDVI Trend')

    # Plot the rolling mean
    ax.plot(anomalies_df['date'], anomalies_df['rolling_mean'], 'g--', label='3-Point Rolling Mean')

    # Highlight anomalies
    anomalous_points = anomalies_df[anomalies_df['is_anomaly']]
    ax.scatter(anomalous_points['date'], anomalous_points['ndvi'], color='red', s=100, zorder=5, label='Anomaly')

    ax.set_title('Simulated NDVI Time Series & Anomaly Detection')
    ax.set_xlabel('Date')
    ax.set_ylabel('Average NDVI')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

if __name__ == '__main__':
    print("--- Testing Temporal Analysis Module (with Simulated Data) ---")

    # 1. Load base data to simulate from
    data_file = 'data/SalinasA.mat'
    gt_file = 'data/SalinasA_gt.mat'
    data_cube, ground_truth = load_salinas_data(data_file, gt_file)

    if data_cube is not None:
        # 2. Simulate the time series
        ts_df = simulate_ndvi_time_series(data_cube, ground_truth)
        print("\nGenerated Time Series:")
        print(ts_df)

        # 3. Artificially create an anomaly for validation
        ts_df_with_anomaly = ts_df.copy()
        anomaly_index = 6
        anomaly_value = ts_df_with_anomaly.loc[anomaly_index, 'ndvi'] * 0.4 # Drastic drop
        ts_df_with_anomaly.loc[anomaly_index, 'ndvi'] = anomaly_value
        print(f"\nArtificially dropped NDVI at index {anomaly_index} to {anomaly_value:.2f} to test detection.")

        # 4. Detect anomalies on the modified data
        analysis_result_df = detect_anomalies(ts_df_with_anomaly, std_dev_threshold=1.0)
        print("\nAnalysis Results:")
        print(analysis_result_df)

        detected_anomalies = analysis_result_df[analysis_result_df['is_anomaly']]

        # 5. Validate detection
        assert not detected_anomalies.empty, "Validation failed: No anomaly was detected."
        assert anomaly_index in detected_anomalies.index, "Validation failed: The correct anomaly was not detected."
        print(f"\n--- Anomaly Detection Test Passed: Correctly flagged anomaly at index {anomaly_index}. ---")

        # 6. Generate and save plot
        fig = plot_temporal_analysis(ts_df_with_anomaly, analysis_result_df)
        output_path = 'temporal_analysis_test.png'
        fig.savefig(output_path)
        print(f"\nTest plot saved to {output_path}")

    else:
        print("\n--- Data Loading Failed, Skipping Temporal Test ---")
