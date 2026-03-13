import pandas as pd
import os

# Paths define karein
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, 'data')
METADATA_PATH = os.path.join(DATA_DIR, 'metadata.csv')

def check_setup():
    print("--- Vigilance Voice AI: Setup Check ---")
    
    # 1. Check CSV
    if os.path.exists(METADATA_PATH):
        df = pd.read_csv(METADATA_PATH)
        print(f"✅ Success: Metadata mili! Total videos: {len(df)}")
        print(df.head(2)) # Pehli 2 rows dikhayega
    else:
        print(f"❌ Error: {METADATA_PATH} nahi mili!")

    # 2. Check Videos Folder
    video_dir = os.path.join(DATA_DIR, 'train_videos')
    if os.path.exists(video_dir):
        videos = os.listdir(video_dir)
        print(f"✅ Success: Video folder mila! Videos ki sankhya: {len(videos)}")
    else:
        print(f"❌ Error: 'train_videos' folder nahi mila!")

if __name__ == "__main__":
    check_setup()