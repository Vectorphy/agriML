# Guide to Downloading Global Satellite Data and Converting to .mat Format

This guide provides a comprehensive workflow for acquiring satellite imagery from major global providers and converting the standard GeoTIFF format into the MATLAB-native `.mat` format.

## Part 1: How to Download Satellite Data (for any Country)

The key to downloading data for any country is to use portals that provide global or near-global coverage. The main free sources are managed by the US Geological Survey (USGS) and the European Space Agency (ESA).

### 1. USGS EarthExplorer

This is one of the most comprehensive portals for satellite and aerial imagery, providing access to datasets like Landsat (global coverage since the 1970s) and Sentinel.

* **What it offers:** Landsat missions (1-9), Sentinel-2, MODIS, and various other earth science datasets.
* **Best for:** Historical analysis, land use change over decades.

#### Step-by-Step Guide:
1.  **Create an Account:** You need a free account to download data. Go to the [USGS EarthExplorer](https://earthexplorer.usgs.gov/) and register.
2.  **Define Area of Interest (AOI):** In the main map interface, define your target area. You can:
    * Click points on the map to draw a polygon.
    * Use the "Address/Place" search bar.
    * Upload a KML or Shapefile.
3.  **Set Date Range:** Specify the start and end dates for your search. This is crucial for temporal analysis.
4.  **Select the Dataset:** Click on the "Data Sets" tab. This is the most important step.
    * For modern, high-quality multispectral data, navigate to **Sentinel -> Sentinel-2**.
    * For long-term historical data, go to **Landsat -> Landsat Collection 2 Level-2**. It is highly recommended to use **Level-2 (Surface Reflectance)** data, as it has been corrected for atmospheric effects and is ready for scientific analysis.
5.  **Add Additional Criteria:**
    * **Cloud Cover:** Set the "Cloud Cover" slider to a low percentage (e.g., < 10%) to get clear images. This is a critical step to ensure data quality.
6.  **Review and Download:**
    * Click the "Results" tab. You will see a list of available images (scenes).
    * Click the foot icon to see the image's footprint on the map and the eye icon for a preview.
    * Click the download icon. For Level-2 data, you will often be presented with a download dialog. Choose the "Product Bundle" or "Download All Bands" option, which will download a `.tar` or `.zip` file containing individual GeoTIFF (`.tif`) files for each spectral band.

### 2. Copernicus Open Access Hub

This is the official portal from the ESA for all Sentinel mission data.

* **What it offers:** Sentinel-1 (Radar), Sentinel-2 (Multispectral), Sentinel-3 (Ocean/Land), Sentinel-5P (Atmosphere).
* **Best for:** High-resolution (10m), recent multispectral data from Sentinel-2.

#### Step-by-Step Guide:
1.  **Create an Account:** Register for a free account at the [Copernicus Open Access Hub](https://scihub.copernicus.eu/).
2.  **Define AOI:** Pan and zoom to your area of interest. Right-click and drag to draw a box.
3.  **Filter Your Search:** Open the search menu (top-left).
    * Set the "Sensing Period" (your date range).
    * Select **"S2MSI2A"** as the "Mission". This is the Level-2A (atmospherically corrected) product, which is ideal for analysis.
    * Set the "Cloud cover percentage" (e.g., from 0 to 10).
4.  **Search and Download:**
    * Click the search icon. A list of products will appear.
    * Click on a product to see its details. Click the download icon to get the full product folder as a `.zip` file.

---

## Part 2: How to Convert Satellite Data into .mat Files

Downloaded satellite data typically comes as a collection of GeoTIFF (`.tif` or `.tiff`) files, where each file represents a single spectral band (e.g., Red, Green, Blue, Near-Infrared). You need to stack these bands into a 3D matrix and save it as a `.mat` file.

### Method 1: Using Python (Recommended)

Python is a free and powerful tool for this task. You'll need two main libraries.

* **Prerequisites:**
    * Python installed.
    * Install required libraries: `pip install rasterio scipy numpy`

* **Python Code:**
    ```python
    import rasterio
    from rasterio.merge import merge
    import numpy as np
    from scipy.io import savemat
    import os

    # --- Configuration ---
    # Path to the directory where you unzipped your satellite data
    # For Sentinel-2, this is often a folder ending in .SAFE/GRANULE/.../IMG_DATA/
    # For Landsat, it's the main folder with all the band files.
    data_directory = 'path/to/your/satellite/bands/'

    # The output .mat file name
    output_mat_file = 'satellite_image.mat'

    # List the band files you want to stack. The order matters!
    # Example for Landsat 8 (B2-B7): Blue, Green, Red, NIR, SWIR1, SWIR2
    # Example for Sentinel-2 (B2-B4, B8): Blue, Green, Red, NIR
    band_files_to_stack = [
        'T36JTT_20250815T074619_B02.jp2', # Blue
        'T36JTT_20250815T074619_B03.jp2', # Green
        'T36JTT_20250815T074619_B04.jp2', # Red
        'T36JTT_20250815T074619_B08.jp2', # NIR
    ]

    # --- Processing ---
    band_paths = [os.path.join(data_directory, f) for f in band_files_to_stack]

    # Open all band files
    src_files_to_mosaic = [rasterio.open(path) for path in band_paths]

    # Merge function can be used if bands are in separate files, which they are.
    # We read them into a single numpy array
    # The result will have the shape (bands, height, width)
    full_image = np.array([src.read(1) for src in src_files_to_mosaic])

    # For MATLAB, it's common to have the shape (height, width, bands)
    # So we transpose the dimensions
    full_image_transposed = full_image.transpose(1, 2, 0)

    print(f"Image stacked. Shape: {full_image_transposed.shape}")

    # Create a dictionary to save in the .mat file
    # The key 'image_cube' will be the variable name in MATLAB
    mat_dict = {'image_cube': full_image_transposed}

    # Save the dictionary to a .mat file
    savemat(output_mat_file, mat_dict)

    print(f"Successfully converted and saved data to {output_mat_file}")

    # Close the files
    for src in src_files_to_mosaic:
        src.close()
    ```

### Method 2: Using MATLAB

If you have MATLAB and the Mapping Toolbox, the process is also straightforward.

* **Prerequisites:**
    * MATLAB installed.
    * **Mapping Toolbox** is required for `geotiffread`.

* **MATLAB Code:**
    ```matlab
    % --- Configuration ---
    % Path to the directory with your satellite data bands
    data_directory = 'C:\path\to\your\satellite\bands\';

    % The output .mat file name
    output_mat_file = 'satellite_image.mat';

    % List the band files you want to stack. The order matters!
    band_files = {
        'LC08_L2SP_148043_20250820_20250828_02_T1_SR_B2.TIF', ... % Blue
        'LC08_L2SP_148043_20250820_20250828_02_T1_SR_B3.TIF', ... % Green
        'LC08_L2SP_148043_20250820_20250828_02_T1_SR_B4.TIF', ... % Red
        'LC08_L2SP_148043_20250820_20250828_02_T1_SR_B5.TIF'      % NIR
    };

    % --- Processing ---
    % Read the first band to get dimensions
    first_band_path = fullfile(data_directory, band_files{1});
    [first_band, ~] = geotiffread(first_band_path);
    [height, width] = size(first_band);
    num_bands = length(band_files);

    % Pre-allocate a 3D matrix for the full image cube
    image_cube = zeros(height, width, num_bands, 'uint16'); % Use the correct data type (e.g., uint16)

    % Loop through each band file, read it, and add it to the 3D matrix
    for i = 1:num_bands
        fprintf('Reading band %d of %d...\n', i, num_bands);
        band_path = fullfile(data_directory, band_files{i});
        image_cube(:, :, i) = geotiffread(band_path);
    end

    fprintf('Image stacked. Size: %s\n', mat2str(size(image_cube)));

    % Save the 3D matrix to a .mat file
    % The variable in the .mat file will be named 'image_cube'
    save(output_mat_file, 'image_cube', '-v7.3'); % '-v7.3' is for large files

    fprintf('Successfully saved data to %s\n', output_mat_file);
    ```
