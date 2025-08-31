import os
from radiant_mlhub import Dataset

# The user might not have set the API key, but we'll try anyway
# as some datasets are public.
if 'MLHUB_API_KEY' not in os.environ:
    print("Warning: MLHUB_API_KEY environment variable not set.")
    print("Attempting to access dataset as a public resource.")

try:
    print("Attempting to download 'ref_south_africa_crops_competition_v1'...")
    dataset = Dataset.fetch('ref_south_africa_crops_competition_v1')

    # This just fetches the dataset metadata, it doesn't download the assets.
    # The documentation for the library is needed to know how to download assets.
    # For now, let's just see if we can even access the dataset.
    print("Successfully fetched dataset metadata:")
    print(dataset.title)
    print(dataset.description)

    print("\nTo download the actual files, I would need to iterate through collections.")
    # Example from docs (conceptual):
    # dataset.download(output_dir='data/sa_crops')
    # This is a large dataset, so let's not do this yet.
    # The goal is just to see if we can connect and get metadata.

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("This likely means an API key is required for this dataset.")
