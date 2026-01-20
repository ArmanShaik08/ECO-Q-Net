#!/usr/bin/env python3
"""
ECO-Q-Net Test Suite
Tests the model on a curated set of labeled images
"""

import os
import sys
from pathlib import Path
from inference.infer import run_inference
import torch
from inference.infer import model, transform, CLASSES, DEVICE
from PIL import Image
import torch.nn.functional as F
from collections import defaultdict

# Test dataset with ground truth labels
TEST_DATASET = {
    "sample.jpeg": "deer",
    "sample 2.jpg": "predator",
    "sample 3.jpg": "predator",
    "sample 4.jpg": "predator",
    "sample 5.jpg": "predator",
    "sample.jpg": "deer",
    "test_deer.jpg": "deer",
    "test_predator.jpg": "predator",
    "test_other.jpg": "other",
}

class ModelTestSuite:
    """Test suite for ECO-Q-Net model"""
    
    def __init__(self):
        self.results = []
        self.confusion_matrix = defaultdict(lambda: defaultdict(int))
        self.metrics = {
            "correct": 0,
            "total": 0,
            "quantum_triggered": 0,
            "by_class": defaultdict(lambda: {"correct": 0, "total": 0})
        }
    
    def test_image(self, image_path, ground_truth):
        """Test a single image"""
        
        if not os.path.exists(image_path):
            return None
        
        try:
            result = run_inference(image_path)
            prediction = result['prediction']
            confidence = result['confidence']
            priority = result['priority']
            risk_score = result['risk_score']
            quantum = result['Conditional Quantumn Usage']
            
            is_correct = (prediction == ground_truth)
            
            # Update metrics
            self.metrics["total"] += 1
            self.metrics["by_class"][ground_truth]["total"] += 1
            
            if is_correct:
                self.metrics["correct"] += 1
                self.metrics["by_class"][ground_truth]["correct"] += 1
            
            if quantum:
                self.metrics["quantum_triggered"] += 1
            
            self.confusion_matrix[ground_truth][prediction] += 1
            
            self.results.append({
                "image": image_path,
                "ground_truth": ground_truth,
                "prediction": prediction,
                "confidence": confidence,
                "priority": priority,
                "risk_score": risk_score,
                "quantum": quantum,
                "correct": is_correct
            })
            
            return result
            
        except Exception as e:
            print(f"Error testing {image_path}: {e}")
            return None
    
    def run_all_tests(self):
        """Run tests on all images in dataset"""
        
        print("=" * 80)
        print("ECO-Q-Net Model Test Suite")
        print("=" * 80)
        print(f"\nTesting {len(TEST_DATASET)} images...\n")
        
        for image_path, ground_truth in sorted(TEST_DATASET.items()):
            print(f"Testing: {image_path:25s} (ground truth: {ground_truth})")
            self.test_image(image_path, ground_truth)
        
        self.print_summary()
    
    def print_summary(self):
        """Print detailed test summary"""
        
        print("\n" + "=" * 80)
        print("TEST RESULTS SUMMARY")
        print("=" * 80)
        
        # Overall accuracy
        accuracy = (self.metrics["correct"] / self.metrics["total"] * 100) if self.metrics["total"] > 0 else 0
        print(f"\n📊 OVERALL ACCURACY: {self.metrics['correct']}/{self.metrics['total']} ({accuracy:.2f}%)")
        
        # Per-class accuracy
        print(f"\n📈 PER-CLASS ACCURACY:")
        for cls in CLASSES:
            stats = self.metrics["by_class"][cls]
            if stats["total"] > 0:
                class_acc = stats["correct"] / stats["total"] * 100
                print(f"   {cls:10s}: {stats['correct']}/{stats['total']} ({class_acc:.2f}%)")
        
        # Confusion matrix
        print(f"\n🔄 CONFUSION MATRIX:")
        print(f"   {'':15s} {'Pred: deer':15s} {'Pred: other':15s} {'Pred: predator':15s}")
        for true_class in CLASSES:
            row = f"   True: {true_class:8s} "
            for pred_class in CLASSES:
                count = self.confusion_matrix[true_class][pred_class]
                row += f" {count:>14d} "
            print(row)
        
        # Quantum usage stats
        print(f"\n🔬 QUANTUM USAGE STATISTICS:")
        print(f"   Total triggered: {self.metrics['quantum_triggered']}/{self.metrics['total']} ({self.metrics['quantum_triggered']/self.metrics['total']*100:.2f}%)")
        
        # Detailed results table
        print(f"\n📋 DETAILED RESULTS:")
        print(f"{'Image':25s} {'Truth':10s} {'Pred':10s} {'Conf':8s} {'Priority':8s} {'Quantum':8s} {'✓/✗':5s}")
        print("-" * 85)
        
        for r in sorted(self.results, key=lambda x: x["image"]):
            status = "✓" if r["correct"] else "✗"
            quantum_str = "YES" if r["quantum"] else "NO"
            print(f"{r['image']:25s} {r['ground_truth']:10s} {r['prediction']:10s} "
                  f"{r['confidence']:7.2%} {r['priority']:8s} {quantum_str:8s} {status:5s}")
        
        print("=" * 80)
    
    def get_misclassifications(self):
        """Return list of misclassified images"""
        return [r for r in self.results if not r["correct"]]
    
    def export_results(self, filepath="test_results.txt"):
        """Export results to file"""
        with open(filepath, "w") as f:
            f.write("ECO-Q-Net Model Test Results\n")
            f.write("=" * 80 + "\n\n")
            
            accuracy = (self.metrics["correct"] / self.metrics["total"] * 100) if self.metrics["total"] > 0 else 0
            f.write(f"Overall Accuracy: {self.metrics['correct']}/{self.metrics['total']} ({accuracy:.2f}%)\n\n")
            
            f.write("Detailed Results:\n")
            f.write("-" * 80 + "\n")
            for r in self.results:
                f.write(f"{r['image']:25s} | Truth: {r['ground_truth']:10s} | "
                       f"Pred: {r['prediction']:10s} | Conf: {r['confidence']:.4f} | "
                       f"Correct: {r['correct']}\n")
        
        print(f"\n✅ Results exported to {filepath}")


def main():
    """Main function"""
    
    suite = ModelTestSuite()
    suite.run_all_tests()
    
    # Export results
    suite.export_results()
    
    # Print misclassifications
    misclassified = suite.get_misclassifications()
    if misclassified:
        print(f"\n⚠️  MISCLASSIFICATIONS ({len(misclassified)} total):")
        for r in misclassified:
            print(f"   {r['image']:25s}: Expected {r['ground_truth']:10s}, Got {r['prediction']:10s} ({r['confidence']:.2%})")


if __name__ == "__main__":
    main()
