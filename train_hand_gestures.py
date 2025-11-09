#!/usr/bin/env python3
"""
VATSAL AI - Hand Gesture Training Utility
Train custom hand gestures for gesture recognition
"""

import sys
import os

# Add module paths
workspace_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(workspace_dir, 'modules')
sys.path.insert(0, workspace_dir)
sys.path.insert(0, modules_dir)
sys.path.insert(0, os.path.join(modules_dir, 'automation'))

from modules.automation.gesture_trainer import GestureTrainer


def print_header():
    """Print welcome header"""
    print("\n" + "=" * 70)
    print("🎓 VATSAL AI - Hand Gesture Training System")
    print("=" * 70)
    print()


def print_menu():
    """Print main menu"""
    print("\n📋 Menu:")
    print("  1. Capture new gesture samples")
    print("  2. Train gesture recognition model")
    print("  3. List existing gestures")
    print("  4. Exit")
    print()


def capture_gesture(trainer: GestureTrainer):
    """Capture samples for a new gesture"""
    print("\n" + "=" * 70)
    print("📸 Capture Gesture Samples")
    print("=" * 70)
    
    gesture_name = input("\nEnter gesture name (e.g., OK_SIGN, THUMBS_DOWN): ").strip().upper()
    
    if not gesture_name:
        print("❌ Gesture name cannot be empty!")
        return
    
    num_samples = input("Number of samples to capture (default: 50): ").strip()
    try:
        num_samples = int(num_samples) if num_samples else 50
    except ValueError:
        num_samples = 50
    
    print(f"\n🎬 Starting capture for '{gesture_name}'...")
    print("Tips:")
    print("  - Position your hand clearly in front of the camera")
    print("  - Use good lighting")
    print("  - Keep the gesture steady")
    print("  - Press SPACE when ready to start capturing")
    print("  - Press ESC to cancel")
    print()
    
    result = trainer.capture_gesture_samples(gesture_name, num_samples)
    
    if result['success']:
        print(f"\n✅ {result['message']}")
        print(f"📁 Samples saved to: {result['save_path']}")
    else:
        print(f"\n❌ {result['message']}")


def train_model(trainer: GestureTrainer):
    """Train the gesture recognition model"""
    print("\n" + "=" * 70)
    print("🧠 Training Gesture Recognition Model")
    print("=" * 70)
    print()
    
    result = trainer.train()
    
    if result['success']:
        print(f"\n✅ {result['message']}")
        print(f"📊 Accuracy: {result['accuracy']:.2f}%")
        print(f"📝 Gestures trained: {result['num_gestures']}")
        print(f"📦 Total samples: {result['num_samples']}")
        print(f"\n🎯 Gesture labels: {list(result['label_mapping'].keys())}")
    else:
        print(f"\n❌ {result['message']}")


def list_gestures(trainer: GestureTrainer):
    """List existing captured gestures"""
    print("\n" + "=" * 70)
    print("📋 Existing Gestures")
    print("=" * 70)
    print()
    
    if not os.path.exists(trainer.training_data_path):
        print("❌ No gestures captured yet!")
        return
    
    gestures = []
    for gesture_name in os.listdir(trainer.training_data_path):
        samples_folder = os.path.join(trainer.training_data_path, gesture_name, "samples")
        if os.path.isdir(samples_folder):
            sample_count = len([f for f in os.listdir(samples_folder) 
                              if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            gestures.append((gesture_name, sample_count))
    
    if not gestures:
        print("❌ No gestures captured yet!")
        return
    
    print(f"Found {len(gestures)} gesture(s):\n")
    for gesture_name, sample_count in sorted(gestures):
        print(f"  ✋ {gesture_name}: {sample_count} samples")
    
    # Check if model is trained
    if os.path.exists(trainer.model_path):
        print(f"\n✅ Trained model exists at: {trainer.model_path}")
    else:
        print(f"\n⚠️  No trained model found. Run 'Train model' to create one.")


def main():
    """Main program loop"""
    print_header()
    
    trainer = GestureTrainer()
    
    print("Welcome to the Hand Gesture Training System!")
    print("This tool helps you train custom hand gestures for VATSAL AI.")
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            capture_gesture(trainer)
        
        elif choice == '2':
            train_model(trainer)
        
        elif choice == '3':
            list_gestures(trainer)
        
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice! Please enter 1-4.")
    
    print("\n" + "=" * 70)
    print("🎓 Training session completed!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Run 'python vatsal.py' to test your trained gestures")
    print("  2. The detector will automatically load your trained model")
    print("  3. Show your custom gestures to the camera to test them!")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Training interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
