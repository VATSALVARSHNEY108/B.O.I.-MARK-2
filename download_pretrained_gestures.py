#!/usr/bin/env python3
"""
Download and Install Pre-trained Hand Gesture Model
This script fetches an open-source pre-trained model and adapts it for VATSAL AI

Run this on your LOCAL Windows/Mac/Linux machine (NOT in Replit)
"""

import urllib.request
import os
import sys

def download_file(url, destination):
    """Download a file from URL"""
    print(f"📥 Downloading from {url}")
    print(f"📁 Saving to {destination}")
    urllib.request.urlretrieve(url, destination)
    print("✅ Download complete!")

def main():
    print("=" * 70)
    print("🎓 VATSAL AI - Pre-trained Gesture Model Downloader")
    print("=" * 70)
    print("\n⚠️  NOTE: This script must be run on your LOCAL machine")
    print("   (Windows/Mac/Linux with camera access)")
    print()
    
    # GitHub raw URLs for the pre-trained model
    base_url = "https://github.com/me2190901/Hand_Gesture_Recognition_Using_SVM/raw/master/"
    model_file = "hog_svm2.pkl"
    
    # Create output directory
    output_dir = "biometric_data/hands/pretrained"
    os.makedirs(output_dir, exist_ok=True)
    
    # Download the model
    model_path = os.path.join(output_dir, model_file)
    
    if os.path.exists(model_path):
        print(f"⚠️  Model already exists at {model_path}")
        response = input("Do you want to re-download? (y/n): ")
        if response.lower() != 'y':
            print("Skipping download.")
            return
    
    try:
        download_file(base_url + model_file, model_path)
        
        print("\n" + "=" * 70)
        print("✅ Pre-trained Model Downloaded Successfully!")
        print("=" * 70)
        print(f"\n📁 Model Location: {model_path}")
        print("\n🎯 This model recognizes 6 hand gestures (labeled 0-5)")
        print("\n💡 Next Steps:")
        print("  1. See README.md in the downloaded folder for gesture labels")
        print("  2. Run the gesture demo to test: python demo_opencv_hand_gesture.py")
        print("  3. Or train your own custom gestures: python train_hand_gestures.py")
        print("\n⚠️  Note: This model uses different feature extraction than")
        print("   the built-in VATSAL system, so it's provided as a reference.")
        print("   For best results, train your own gestures using")
        print("   'python train_hand_gestures.py'")
        print()
        
    except Exception as e:
        print(f"\n❌ Error downloading model: {e}")
        print("\nAlternative: Download manually from:")
        print(f"  {base_url}{model_file}")
        print(f"  Save to: {model_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
