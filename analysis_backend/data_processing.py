import scipy.io
import numpy as np

def load_salinas_data(data_path, gt_path=None):
    """
    Loads the Salinas hyperspectral data and, optionally, its ground truth map.

    Args:
        data_path (str): The file path to the Salinas .mat data file.
        gt_path (str, optional): The file path to the Salinas ground truth .mat file. Defaults to None.

    Returns:
        tuple: A tuple containing:
            - data_cube (np.ndarray): The hyperspectral data cube.
            - ground_truth (np.ndarray or None): The ground truth map, or None if not provided/found.
    """
    data_cube, ground_truth = None, None
    try:
        data_mat = scipy.io.loadmat(data_path)
        data_key = [k for k in data_mat.keys() if not k.startswith('__')][0]
        data_cube = data_mat[data_key]
        print(f"Data cube loaded with shape: {data_cube.shape}")
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        return None, None
    except Exception as e:
        print(f"An error occurred while loading the data cube: {e}")
        return None, None

    if gt_path:
        try:
            gt_mat = scipy.io.loadmat(gt_path)
            gt_key = [k for k in gt_mat.keys() if not k.startswith('__')][0]
            ground_truth = gt_mat[gt_key]
            print(f"Ground truth loaded with shape: {ground_truth.shape}")
        except FileNotFoundError:
            print(f"Warning: Ground truth file not found at {gt_path}")
        except Exception as e:
            print(f"An error occurred while loading the ground truth: {e}")

    return data_cube, ground_truth

if __name__ == '__main__':
    # Example usage for testing the function
    # Note: This assumes the data is in a 'data' subdirectory relative to the project root.
    data_file = 'data/SalinasA.mat'
    gt_file = 'data/SalinasA_gt.mat'

    hyperspectral_data, gt_data = load_salinas_data(data_file, gt_file)

    if hyperspectral_data is not None:
        print("\n--- Data Loading Test Successful ---")
        print(f"Data type: {type(hyperspectral_data)}")
        print(f"Data dimensions: {hyperspectral_data.ndim}")
        # Validate dimensions (should be 3 for a data cube)
        assert hyperspectral_data.ndim == 3
        # Validate ground truth dimensions (should be 2)
        assert gt_data.ndim == 2
        print("Validation checks passed.")

    else:
        print("\n--- Data Loading Test Failed ---")
