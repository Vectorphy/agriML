# Author: Jules
#
# © 2025 Jules
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

import pandas as pd

# Load the training data CSV
try:
    df = pd.read_csv('data/field_info_train.csv')
    print("Successfully loaded data/field_info_train.csv")
    print("First 5 rows:")
    print(df.head())
    print("\nColumns:")
    print(df.columns)
    print("\nInfo:")
    df.info()
except FileNotFoundError:
    print("Error: Could not find data/field_info_train.csv")
except Exception as e:
    print(f"An error occurred: {e}")
