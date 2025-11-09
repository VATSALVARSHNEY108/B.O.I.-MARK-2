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
    readme_url = "https://github.com/me2190901/Hand_Gesture_Recognition_Using_SVM/raw/master/README.md"
    model_file = "hog_svm2.pkl"
    
    # Create output directory
    output_dir = "biometric_data/hands/pretrained"
    os.makedirs(output_dir, exist_ok=True)
    
    # Download the model
    model_path = os.path.join(output_dir, model_file)
    readme_path = os.path.join(output_dir, "REFERENCE_README.md")
    
    if os.path.exists(model_path):
        print(f"⚠️  Model already exists at {model_path}")
        response = input("Do you want to re-download? (y/n): ")
        if response.lower() != 'y':
            print("Skipping download.")
            return
    
    try:
        # Download model and README
        download_file(base_url + model_file, model_path)
        print()
        download_file(readme_url, readme_path)
        
        # Create local README with integration notes
        local_readme_path = os.path.join(output_dir, "README.md")
        with open(local_readme_path, 'w') as f:
            f.write("# Pre-trained Gesture Model (Reference Only)\n\n")
            f.write("## Model Information\n")
            f.write("- **File:** hog_svm2.pkl\n")
            f.write("- **Gestures:** 6 hand gestures (labeled 0-5)\n")
            f.write("- **Accuracy:** 87.66%\n")
            f.write("- **Source:** https://github.com/me2190901/Hand_Gesture_Recognition_Using_SVM\n\n")
            f.write("## ⚠️ Important Notes\n\n")
            f.write("This model is **for reference and experimentation only**.\n\n")
            f.write("**Why?**\n")
            f.write("- Uses different feature extraction (Canny + HOG)\n")
            f.write("- Not compatible with VATSAL's default pipeline\n")
            f.write("- Requires custom integration code to use\n\n")
            f.write("## ✅ Recommended Approach\n\n")
            f.write("**Instead of using this model**, we recommend:\n\n")
            f.write("1. **Use MediaPipe gestures** (already working, 7 gestures!):\n")
            f.write("   - Open_Palm, Closed_Fist, Thumbs_Up, Thumbs_Down, etc.\n")
            f.write("   - Run: `python demo_opencv_hand_gesture.py`\n\n")
            f.write("2. **Train your own custom gestures** (best results!):\n")
            f.write("   - Perfectly tuned to your hand/camera/lighting\n")
            f.write("   - Takes 5-10 minutes\n")
            f.write("   - Run: `python train_hand_gestures.py`\n\n")
            f.write("## Gesture Labels (From Original Model)\n\n")
            f.write("The model recognizes 6 gestures with numeric labels 0-5.\n")
            f.write("See REFERENCE_README.md for the original documentation.\n\n")
            f.write("## To Use This Model\n\n")
            f.write("You would need to:\n")
            f.write("1. Create custom feature extraction matching the model's format\n")
            f.write("2. Write integration code to load and use this SVM classifier\n")
            f.write("3. Map numeric labels (0-5) to gesture names\n\n")
            f.write("This is provided as a learning resource. For production use,\n")
            f.write("train custom gestures with the built-in trainer!\n")
        
        print("\n" + "=" * 70)
        print("✅ Files Downloaded Successfully!")
        print("=" * 70)
        print(f"\n📁 Downloaded to: {output_dir}/")
        print(f"   • {model_file} - SVM classifier (2.2MB)")
        print(f"   • README.md - Integration guide & warnings")
        print(f"   • REFERENCE_README.md - Original documentation")
        
        print("\n" + "=" * 70)
        print("⚠️  IMPORTANT: This Model is For Reference Only!")
        print("=" * 70)
        print("\n❌ This model will NOT work with VATSAL's default gesture system because:")
        print("   • Uses different feature extraction (Canny edges + HOG)")
        print("   • Requires custom integration code to use")
        print("   • Uses numeric labels (0-5) instead of gesture names")
        print("\n💡 To actually USE this model, you would need to:")
        print("   1. Study the original code: Final.py from the GitHub repo")
        print("   2. Write custom feature extraction matching their format")
        print("   3. Create integration code to load and call this SVM")
        print("   4. Map numeric outputs to gesture names")
        
        print("\n" + "=" * 70)
        print("✅ RECOMMENDED: Use These Instead (Already Working!)")
        print("=" * 70)
        print("\n🚀 Option 1: MediaPipe Gestures (7 gestures, zero setup!)")
        print("   Run: python demo_opencv_hand_gesture.py")
        print("   Gestures: Open_Palm, Thumbs_Up, Victory, etc.")
        print("\n🎯 Option 2: Train Custom Gestures (unlimited, best accuracy!)")
        print("   Run: python train_hand_gestures.py")
        print("   Takes 5-10 minutes, perfectly tuned to YOUR hand/camera")
        
        print("\n" + "=" * 70)
        print(f"📖 For full details, read: {output_dir}/README.md")
        print("=" * 70)
        print()
        
    except Exception as e:
        print(f"\n❌ Error downloading model: {e}")
        print("\nAlternative: Download manually from:")
        print(f"  {base_url}{model_file}")
        print(f"  Save to: {model_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
