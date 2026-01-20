# ECO Q-Net 

ECO Q‑Net is a risk‑aware wildlife monitoring and decision‑support system designed for analyzing camera‑trap images under real‑world uncertainty. The project uses a deep learning model for animal classification and augments it with confidence‑aware inference, ecological risk scoring, and priority‑based decision logic. High‑risk and low‑confidence cases trigger conditional Set‑6 (quantum) escalation, ensuring that critical monitoring scenarios receive additional attention. The system is deployed as a web application using FastAPI with a Figma‑based user interface, demonstrating an end‑to‑end, deployment‑ready prototype.

##  Key Features
- CNN-based wildlife classification
- Confidence-aware inference
- Ecological risk scoring (LOW / MEDIUM / HIGH)
- Conditional Set-6 (Quantum) escalation
- Web interface using FastAPI + Figma UI

##  System Pipeline
Image → Classification → Confidence → Risk Score → Priority → Conditional Escalation

## 📂 Project Structure
ECO-Q-Net/
│── backend/ # FastAPI backend

│── dataset/ # Dataset preprocessing scripts

│── training/ # Model training scripts

│── inference/ # Inference + decision logic

│── frontend/ # Figma-based UI

│── data/ 

## Setup Instructions
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Initialize Git Locally

From the **project root**:

```bash
git init
git status
