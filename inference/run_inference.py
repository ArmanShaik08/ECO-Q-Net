#!/usr/bin/env python3
"""
Generalized inference runner for ECO-Q-Net
Usage: python run_inference.py <image_path>
"""

import sys
import os
from inference.infer import run_inference
import torch
from inference.infer import model, transform, CLASSES, DEVICE
from PIL import Image
import torch.nn.functional as F

def print_detailed_results(image_path):
    """Run inference and print detailed results"""
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image '{image_path}' not found")
        return False
    
    print("=" * 70)
    print(f"ECO-Q-Net Inference")
    print("=" * 70)
    print(f"Image: {image_path}")
    print(f"Device: {DEVICE}")
    print("-" * 70)
    
    try:
        # Run inference
        result = run_inference(image_path)
        
        # Print main results
        print(f"\n📊 PREDICTION RESULTS:")
        print(f"   Class: {result['prediction'].upper()}")
        print(f"   Confidence: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)")
        print(f"   Priority: {result['priority']}")
        print(f"   Risk Score: {result['risk_score']:.4f}")
        
        # Get detailed probabilities
        image = Image.open(image_path).convert("RGB")
        x = transform(image).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            logits = model(x)
            probs = F.softmax(logits, dim=1)
        
        print(f"\n📈 CLASS PROBABILITIES:")
        for i, class_name in enumerate(CLASSES):
            prob = probs[0][i].item()
            bar = "█" * int(prob * 40)
            print(f"   {class_name:10s}: {prob:.4f} ({prob*100:5.2f}%) {bar}")
        
        # Conditional Quantum Usage
        print(f"\n" + "-" * 70)
        quantum = result['Conditional Quantumn Usage']
        print(f"🔬 CONDITIONAL QUANTUM USAGE: {quantum}")
        
        if quantum:
            print(f"   ✅ QUANTUM PROCESSING ACTIVATED")
            print(f"   Reason: High-risk prediction with low confidence")
            print(f"   Action: Escalate to quantum-enhanced classification")
        else:
            print(f"   Standard classical processing sufficient")
        
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"❌ Error during inference: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python run_inference.py <image_path>")
        print("\nExamples:")
        print("  python run_inference.py sample.jpg")
        print("  python run_inference.py 'sample 5.jpg'")
        print("  python run_inference.py /path/to/image.jpg")
        print("\nAvailable sample images:")
        samples = [f for f in os.listdir('.') if f.startswith('sample') and f.endswith(('.jpg', '.jpeg', '.png'))]
        for s in sorted(samples):
            print(f"  - {s}")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = print_detailed_results(image_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
