#!/usr/bin/env python3
"""
Train VATSAL AI to Recognize Your Face
Uses your photos to create a personalized face recognition model
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

from modules.automation.face_trainer import FaceTrainer


def main():
    print("=" * 70)
    print("VATSAL AI - Personal Face Recognition Training")
    print("=" * 70)
    print()
    print("This will train the system to recognize YOUR face!")
    print()
    print("📂 Training Data Location:")
    print("  biometric_data/faces/vatsal/training/")
    print()
    print("📸 Your Photos:")
    print("  ✅ 7 photos copied from attached_assets/")
    print()
    print("=" * 70)
    print()
    
    # Create trainer
    trainer = FaceTrainer("biometric_data/faces")
    
    # Train the model
    result = trainer.train()
    
    if result['success']:
        print("\n" + "=" * 70)
        print("🎉 SUCCESS! Your face model is trained!")
        print("=" * 70)
        print()
        print(f"📊 Training Results:")
        print(f"  Face samples processed: {result['samples']}")
        print(f"  People in model: {result['people']}")
        print(f"  Model file: {result['model_path']}")
        print()
        print("🎯 The system will now:")
        print("  1. Detect your face in real-time")
        print("  2. Recognize you as 'VATSAL'")
        print("  3. Greet you by name when you appear")
        print()
        print("=" * 70)
        print("\n✅ Next Steps:")
        print("  1. Run: python test_face_recognition.py")
        print("  2. Or use in main app: streamlit run vatsal.py")
        print()
        print("The system is now personalized for you! 🚀")
        
    else:
        print(f"\n❌ Training failed: {result['message']}")
        print("\n💡 Make sure photos are in:")
        print("  biometric_data/faces/vatsal/training/")


if __name__ == "__main__":
    main()
