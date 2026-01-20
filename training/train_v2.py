import os
import sys
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from collections import Counter
from tqdm import tqdm

print("Starting training script...", flush=True)
sys.stdout.flush()

# CONFIG
DATA_DIR = "data/processed"
BATCH_SIZE = 128
EPOCHS = 1
LR = 0.001  
MAX_TRAIN_BATCHES = 60  # cap batches per epoch to finish within ~30-40 minutes on CPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"DATA_DIR: {DATA_DIR}", flush=True)
print(f"DEVICE: {DEVICE}", flush=True)
print(f"BATCH_SIZE: {BATCH_SIZE}", flush=True)
print(f"EPOCHS: {EPOCHS}", flush=True)

# TRANSFORMS with aggressive augmentation
train_tf = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(20),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# DATASETS
print("\nLoading datasets...", flush=True)
train_ds = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=train_tf)
val_ds   = datasets.ImageFolder(os.path.join(DATA_DIR, "val"), transform=val_tf)

print(f"✅ Train dataset: {len(train_ds)} samples", flush=True)
print(f"✅ Val dataset: {len(val_ds)} samples", flush=True)

train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
val_loader   = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

class_names = train_ds.classes
print(f"Classes: {class_names}", flush=True)

# CLASS WEIGHTS
counts = Counter(train_ds.targets)
total = sum(counts.values())
class_weights = [(total / counts[i]) ** 1.5 for i in range(len(class_names))]
class_weights = torch.tensor(class_weights, dtype=torch.float).to(DEVICE)
print(f"Class weights: {class_weights}", flush=True)

# MODEL
print("\nLoading MobileNetV2...", flush=True)
model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
print("✅ Model loaded", flush=True)
model.classifier[1] = nn.Linear(model.last_channel, len(class_names))
print("✅ Classifier replaced", flush=True)
model = model.to(DEVICE)
print(f"✅ Model moved to {DEVICE}", flush=True)

# LOSS + OPTIMIZER
criterion = nn.CrossEntropyLoss(weight=class_weights)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)
print("✅ Loss and optimizer ready", flush=True)

# TRAIN LOOP
best_val_acc = 0.0
print(f"\n🔄 Starting training ({EPOCHS} epochs)...\n", flush=True)

for epoch in range(EPOCHS):
    print(f"\nEpoch [{epoch+1}/{EPOCHS}]", flush=True)
    model.train()
    running_loss = 0.0
    train_batches = min(len(train_loader), MAX_TRAIN_BATCHES)
    
    # Training with progress bar
    pbar = tqdm(train_loader, desc="Training", unit="batch")
    for batch_idx, (x, y) in enumerate(pbar):
        if batch_idx >= MAX_TRAIN_BATCHES:
            break
        x, y = x.to(DEVICE), y.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(x)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if pbar.n > 0:
            pbar.set_postfix({"loss": f"{running_loss/pbar.n:.4f}"})

    # VALIDATION
    print("Validating...", flush=True)
    model.eval()
    correct, total_samples = 0, 0

    val_pbar = tqdm(val_loader, desc="Validation", unit="batch")
    with torch.no_grad():
        for x, y in val_pbar:
            x, y = x.to(DEVICE), y.to(DEVICE)
            outputs = model(x)
            _, preds = torch.max(outputs, 1)

            correct += (preds == y).sum().item()
            total_samples += y.size(0)
            val_pbar.set_postfix({"acc": f"{correct/total_samples:.4f}"})

    val_acc = correct / total_samples
    avg_loss = running_loss / max(train_batches, 1)

    print(f"\n  Loss: {avg_loss:.4f} | Val Acc: {val_acc:.4f}", flush=True)

    # Save best model
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), "ecoqnet_best.pth")
        print(f"  ✅ Best model saved (acc: {val_acc:.4f})", flush=True)

print(f"\n Training complete. Best Val Acc: {best_val_acc:.4f}", flush=True)
