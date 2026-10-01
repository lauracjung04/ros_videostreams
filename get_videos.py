from datasets import load_dataset
import json
import os

# Load the dataset in streaming mode
dataset = load_dataset("HuggingFaceFV/finevideo", split="train", streaming=True)

# Define the category you want to filter by
desired_category = 'Biology'  # Replace with your desired category

#specifically for a fine category
def is_desired_category(sample):
    return sample['json']['content_fine_category'] == desired_category

filtered_dataset = filter(is_desired_category, dataset)

# Create directories to save videos and metadata
os.makedirs("videos", exist_ok=True)
os.makedirs("metadata", exist_ok=True)

for idx, sample in enumerate(filtered_dataset):
    video_filename = f"videos/sample_{idx}.mp4"
    with open(video_filename, 'wb') as video_file:
        video_file.write(sample['mp4'])

    json_filename = f"metadata/sample_{idx}.json"
    with open(json_filename, 'w') as json_file:
        json.dump(sample['json'], json_file)

    print(f"Got sample {idx}", flush=True)

    if idx >= 9:  # Limit to 10 samples
        break