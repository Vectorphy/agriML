import numpy as np

def calculate_ndvi(data_cube):
    """
    Calculates the Normalized Difference Vegetation Index (NDVI).
    NDVI = (NIR - Red) / (NIR + Red)
    """
    # Bands for AVIRIS sensor (0-indexed)
    # Red: Band 31 (660.7 nm)
    # NIR: Band 53 (859.5 nm)
    red_band = data_cube[:, :, 31].astype(float)
    nir_band = data_cube[:, :, 53].astype(float)

    epsilon = 1e-10
    ndvi = (nir_band - red_band) / (nir_band + red_band + epsilon)
    return ndvi

def calculate_savi(data_cube):
    """
    Calculates the Soil-Adjusted Vegetation Index (SAVI).
    SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L)
    """
    # Red: Band 31 (660.7 nm)
    # NIR: Band 53 (859.5 nm)
    L = 0.5  # Soil brightness correction factor
    red_band = data_cube[:, :, 31].astype(float)
    nir_band = data_cube[:, :, 53].astype(float)

    epsilon = 1e-10
    savi = ((nir_band - red_band) / (nir_band + red_band + L + epsilon)) * (1 + L)
    return savi

def calculate_ndwi(data_cube):
    """
    Calculates the Normalized Difference Water Index (NDWI).
    NDWI = (NIR - SWIR) / (NIR + SWIR)
    """
    # NIR: Band 53 (859.5 nm)
    # SWIR: Band 135 (1650 nm)
    nir_band = data_cube[:, :, 53].astype(float)
    swir_band = data_cube[:, :, 135].astype(float)

    epsilon = 1e-10
    ndwi = (nir_band - swir_band) / (nir_band + swir_band + epsilon)
    return ndwi

def calculate_ndre(data_cube):
    """
    Calculates the Normalized Difference Red Edge Index (NDRE).
    NDRE = (NIR - Red Edge) / (NIR + Red Edge)
    """
    # NIR: Band 53 (859.5 nm)
    # Red Edge: Band 38 (717.0 nm)
    nir_band = data_cube[:, :, 53].astype(float)
    red_edge_band = data_cube[:, :, 38].astype(float)

    epsilon = 1e-10
    ndre = (nir_band - red_edge_band) / (nir_band + red_edge_band + epsilon)
    return ndre

if __name__ == '__main__':
    # Create a dummy data cube for testing
    # Shape: (height, width, bands)
    dummy_cube = np.random.rand(10, 10, 224) * 255
    dummy_cube = dummy_cube.astype(np.uint16)

    print("--- Testing Index Calculations ---")

    ndvi_map = calculate_ndvi(dummy_cube)
    print(f"NDVI map shape: {ndvi_map.shape}, Min: {np.min(ndvi_map):.2f}, Max: {np.max(ndvi_map):.2f}")
    assert ndvi_map.shape == (10, 10)

    savi_map = calculate_savi(dummy_cube)
    print(f"SAVI map shape: {savi_map.shape}, Min: {np.min(savi_map):.2f}, Max: {np.max(savi_map):.2f}")
    assert savi_map.shape == (10, 10)

    ndwi_map = calculate_ndwi(dummy_cube)
    print(f"NDWI map shape: {ndwi_map.shape}, Min: {np.min(ndwi_map):.2f}, Max: {np.max(ndwi_map):.2f}")
    assert ndwi_map.shape == (10, 10)

    ndre_map = calculate_ndre(dummy_cube)
    print(f"NDRE map shape: {ndre_map.shape}, Min: {np.min(ndre_map):.2f}, Max: {np.max(ndre_map):.2f}")
    assert ndre_map.shape == (10, 10)

    print("\n--- All Index Calculation Tests Passed ---")
