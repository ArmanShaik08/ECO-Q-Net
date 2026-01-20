import os
import shutil

# Correct Kaggle path (Set1 is important)
KAGGLE_BASE = "/Users/armanshaik/.cache/kagglehub/datasets/silviamatoke/serengeti-dataset/versions/1/Set1"
PROJECT_RAW = "data/raw"

# ECO-Q-Net ecological grouping
CLASS_MAP = {
    "deer": [
        "Roe_Deer",
        "Red_Deer",
        "White_Tailed_Deer",
        "Red_Brocket_Deer"
    ],
    "predator": [
        "Ocelot",
        "Red_Fox",
        "Wild_Boar"
    ],
    "other": [
        "Wood_Mouse",
        "Red_Squirrel",
        "European_Hare",
        "Bird_spec",
        "Paca",
        "Agouti"
    ]
}

# Create output folders
for cls in CLASS_MAP:
    os.makedirs(os.path.join(PROJECT_RAW, cls), exist_ok=True)

print("Scanning Kaggle Set1 dataset...")

for folder in os.listdir(KAGGLE_BASE):
    folder_path = os.path.join(KAGGLE_BASE, folder)
    if not os.path.isdir(folder_path):
        continue

    # Example folder: "1.58-Roe_Deer"
    species = folder.split("-", 1)[-1]

    for target_class, species_list in CLASS_MAP.items():
        if species in species_list:
            count = 0
            for root, dirs, files in os.walk(folder_path):
                for img in files:
                    src_file = os.path.join(root, img)
                    dst_file = os.path.join(PROJECT_RAW, target_class, img)
                    shutil.copy(src_file, dst_file)
                    count += 1
            print(f"✅ {species} → {target_class} ({count} images)")

print("🎉 Dataset successfully mapped and imported.")
