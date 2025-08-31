import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

def classify_pixels(data_cube, ground_truth):
    """
    Trains a Random Forest classifier and classifies the hyperspectral data.

    Args:
        data_cube (np.ndarray): The hyperspectral data cube.
        ground_truth (np.ndarray): The ground truth map.

    Returns:
        tuple: A tuple containing:
            - classification_map (np.ndarray): The 2D map of predicted classes.
            - metrics (dict): A dictionary with performance metrics.
    """
    # Reshape the data for classification
    # Flatten the spatial dimensions (height, width) into a single list of pixels
    h, w, bands = data_cube.shape
    X = data_cube.reshape((h * w, bands))

    # Flatten the ground truth map
    y = ground_truth.ravel()

    # Filter out un-labeled pixels (class 0)
    # The model should only be trained on pixels with known labels
    X_labeled = X[y != 0]
    y_labeled = y[y != 0]

    if len(y_labeled) == 0:
        print("No labeled data available for training.")
        return None, None

    # Split the labeled data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_labeled, y_labeled, test_size=0.3, random_state=42, stratify=y_labeled
    )

    # Initialize and train the Random Forest classifier
    print("Training Random Forest classifier...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    print("Training complete.")

    # Evaluate the model on the test set
    y_pred_test = rf.predict(X_test)

    metrics = {
        "overall_accuracy": accuracy_score(y_test, y_pred_test),
        "precision": precision_score(y_test, y_pred_test, average='weighted'),
        "recall": recall_score(y_test, y_pred_test, average='weighted'),
        "confusion_matrix": confusion_matrix(y_test, y_pred_test).tolist() # convert to list for easy display
    }

    # Predict the class for every pixel in the entire cube
    print("Generating full classification map...")
    y_pred_full = rf.predict(X)
    classification_map = y_pred_full.reshape((h, w))
    print("Classification map generated.")

    # Set unlabeled pixels (class 0 in ground truth) back to 0 in the classification map
    classification_map[ground_truth == 0] = 0

    return classification_map, metrics

if __name__ == '__main__':
    # This test requires the data loading functions
    from data_processing import load_salinas_data

    print("--- Testing Classification Module ---")
    data_file = 'data/SalinasA.mat'
    gt_file = 'data/SalinasA_gt.mat'

    data_cube, ground_truth = load_salinas_data(data_file, gt_file)

    if data_cube is not None and ground_truth is not None:
        class_map, perf_metrics = classify_pixels(data_cube, ground_truth)

        if class_map is not None:
            print("\n--- Classification Test Successful ---")
            print(f"Classification map shape: {class_map.shape}")
            assert class_map.shape == (data_cube.shape[0], data_cube.shape[1])

            print("\nPerformance Metrics:")
            for key, value in perf_metrics.items():
                if key != "confusion_matrix":
                    print(f"  {key}: {value:.4f}")
            print(f"  Confusion Matrix:\n{np.array(perf_metrics['confusion_matrix'])}")

            # Check that the unlabeled pixels are still 0
            assert np.all(class_map[ground_truth == 0] == 0)
            print("\nValidation checks passed.")
        else:
            print("\n--- Classification Test Failed ---")
    else:
        print("\n--- Data Loading Failed, Skipping Classification Test ---")
