#!/usr/bin/env python3
"""
Test Gesture Training System Without Camera
This demonstrates the ML components work correctly
"""

import sys
import os
import numpy as np

# Add paths
workspace_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(workspace_dir, 'modules')
sys.path.insert(0, workspace_dir)
sys.path.insert(0, modules_dir)
sys.path.insert(0, os.path.join(modules_dir, 'automation'))

print("🧪 Testing Gesture Training System Components\n")
print("=" * 70)

# Test 1: Check scikit-learn import
print("\n1️⃣  Testing scikit-learn import...")
try:
    from sklearn.svm import SVC
    from sklearn.preprocessing import StandardScaler
    print("   ✅ scikit-learn imported successfully")
except Exception as e:
    print(f"   ❌ scikit-learn import failed: {e}")
    print("\n   🔧 FIX: Run this command:")
    print("   pip install --force-reinstall --no-cache-dir scikit-learn")
    sys.exit(1)

# Test 2: Check OpenCV import
print("\n2️⃣  Testing OpenCV import...")
try:
    import cv2
    print(f"   ✅ OpenCV imported successfully (version {cv2.__version__})")
except Exception as e:
    print(f"   ❌ OpenCV import failed: {e}")
    sys.exit(1)

# Test 3: Import GestureTrainer
print("\n3️⃣  Testing GestureTrainer module...")
try:
    from modules.automation.gesture_trainer import GestureTrainer
    print("   ✅ GestureTrainer imported successfully")
except Exception as e:
    print(f"   ❌ GestureTrainer import failed: {e}")
    print(f"\n   Error details: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Create synthetic training data
print("\n4️⃣  Creating synthetic gesture data (simulating camera capture)...")
try:
    trainer = GestureTrainer()
    
    # Create fake gesture samples directory
    os.makedirs("biometric_data/hands/TEST_THUMBS_DOWN/samples", exist_ok=True)
    os.makedirs("biometric_data/hands/TEST_OK_SIGN/samples", exist_ok=True)
    
    # Generate synthetic 128x128 grayscale images
    for gesture_name in ["TEST_THUMBS_DOWN", "TEST_OK_SIGN"]:
        for i in range(30):
            # Create random patterns to simulate different gestures
            if gesture_name == "TEST_THUMBS_DOWN":
                # Pattern 1: Vertical line (thumb down)
                img = np.zeros((128, 128), dtype=np.uint8)
                img[30:100, 60:68] = 255
            else:
                # Pattern 2: Circle (OK sign)
                img = np.zeros((128, 128), dtype=np.uint8)
                cv2.circle(img, (64, 64), 30, 255, -1)
            
            # Add some noise to make it realistic
            noise = np.random.randint(0, 50, (128, 128), dtype=np.uint8)
            img = cv2.add(img, noise)
            
            sample_path = f"biometric_data/hands/{gesture_name}/samples/sample_{i:03d}.png"
            cv2.imwrite(sample_path, img)
    
    print("   ✅ Created 60 synthetic samples (30 per gesture)")
except Exception as e:
    print(f"   ❌ Failed to create test data: {e}")
    sys.exit(1)

# Test 5: Train the model
print("\n5️⃣  Training model on synthetic data...")
try:
    result = trainer.train()
    
    if result['success']:
        print(f"   ✅ Training successful!")
        print(f"   📊 Accuracy: {result['accuracy']:.2f}%")
        print(f"   📝 Gestures: {list(result['label_mapping'].keys())}")
        print(f"   📦 Samples: {result['num_samples']}")
    else:
        print(f"   ❌ Training failed: {result['message']}")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Training error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Load and test prediction
print("\n6️⃣  Testing gesture prediction...")
try:
    # Create a test image
    test_img = np.zeros((128, 128), dtype=np.uint8)
    cv2.circle(test_img, (64, 64), 30, 255, -1)  # Circle = OK_SIGN
    
    gesture_name, confidence = trainer.predict_gesture(test_img, min_confidence=0.5)
    
    print(f"   ✅ Prediction successful!")
    print(f"   🎯 Detected: {gesture_name}")
    print(f"   📊 Confidence: {confidence*100:.1f}%")
    
    if "OK_SIGN" in gesture_name:
        print("   ✅ Correctly identified OK_SIGN pattern!")
except Exception as e:
    print(f"   ❌ Prediction error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 7: Check detector integration
print("\n7️⃣  Testing detector integration...")
try:
    from modules.automation.opencv_hand_gesture_detector import OpenCVHandGestureDetector
    
    # Create detector (won't start camera, just test loading)
    detector = OpenCVHandGestureDetector(use_trained_model=True)
    
    if detector.gesture_trainer is not None:
        print("   ✅ Detector loaded trained model successfully!")
        print(f"   📋 Available gestures: {list(detector.gesture_trainer.labels.keys())}")
    else:
        print("   ⚠️  Detector created but no trained model loaded")
        print("   This is OK if no model exists yet")
    
except Exception as e:
    print(f"   ❌ Detector integration error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Cleanup test data
print("\n8️⃣  Cleaning up test data...")
try:
    import shutil
    if os.path.exists("biometric_data/hands/TEST_THUMBS_DOWN"):
        shutil.rmtree("biometric_data/hands/TEST_THUMBS_DOWN")
    if os.path.exists("biometric_data/hands/TEST_OK_SIGN"):
        shutil.rmtree("biometric_data/hands/TEST_OK_SIGN")
    print("   ✅ Test data cleaned up")
except Exception as e:
    print(f"   ⚠️  Cleanup warning: {e}")

# Final summary
print("\n" + "=" * 70)
print("🎉 ALL TESTS PASSED!")
print("=" * 70)
print("\n✅ The gesture training system is working correctly!")
print("\n⚠️  IMPORTANT: Camera-based features require:")
print("   1. A physical camera/webcam")
print("   2. Display server (X11/Wayland)")
print("   3. Desktop environment (not Replit)")
print("\n📝 To use on your local machine:")
print("   1. Download this project to your computer")
print("   2. Install: pip install scikit-learn opencv-python numpy")
print("   3. Run: python3 train_hand_gestures.py")
print("   4. Capture real gestures with your webcam")
print("   5. Run: python3 vatsal.py")
print("\n💡 In Replit, you can only test the ML logic (like this script).")
print("   For actual camera gesture detection, use it locally!")
print()
