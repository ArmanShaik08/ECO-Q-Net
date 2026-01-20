import os

PROJECT_NAME = "ECO-Q-Net"

# Helper function
def make(path):
    os.makedirs(path, exist_ok=True)

# =========================
# Root project
# =========================
make(PROJECT_NAME)

# =========================
# DATA FOLDERS
# =========================
data_root = f"{PROJECT_NAME}/data"

make(f"{data_root}/metadata")
make(f"{data_root}/raw")
make(f"{data_root}/processed")

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
classes = CLASS_MAP.keys()  
splits = ["train", "val", "test"]

# Raw class folders
for cls in classes:
    make(f"{data_root}/raw/{cls}")

# Processed split folders
for split in splits:
    for cls in classes:
        make(f"{data_root}/processed/{split}/{cls}")

# =========================
# DATASET SCRIPTS
# =========================
make(f"{PROJECT_NAME}/dataset")

# =========================
# MODEL FOLDERS
# =========================
make(f"{PROJECT_NAME}/models")

# =========================
# PRIORITY + DECISION LOGIC
# =========================
make(f"{PROJECT_NAME}/priority")
make(f"{PROJECT_NAME}/decision")

# =========================
# TRAINING / INFERENCE
# =========================
make(f"{PROJECT_NAME}/training")
make(f"{PROJECT_NAME}/inference")

# =========================
# WEB APPLICATION
# =========================
make(f"{PROJECT_NAME}/backend")
make(f"{PROJECT_NAME}/backend/api")
make(f"{PROJECT_NAME}/backend/core")

make(f"{PROJECT_NAME}/frontend")

# =========================
# VISUALIZATION
# =========================
make(f"{PROJECT_NAME}/visualization")

# =========================
# DOCUMENTATION
# =========================
make(f"{PROJECT_NAME}/docs")
make(f"{PROJECT_NAME}/docs/architecture_diagrams")

print("✅ ECO Q-Net folder structure created successfully.")
