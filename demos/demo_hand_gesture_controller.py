"""
Demo: Hand Gesture Mouse Controller
Demonstrates all hand gesture control capabilities
"""

import sys
from modules.automation.hand_gesture_controller import HandGestureController


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def show_gestures_guide():
    """Show comprehensive gestures guide"""
    print_header("HAND GESTURE CONTROLS GUIDE")
    
    print("""
✋ BASIC GESTURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 👆 CURSOR MOVEMENT
   └─ Index finger UP (alone)
   └─ OR Index + Middle fingers UP
   └─ Move your hand to control the cursor
   └─ Smooth tracking with minimal jitter

2. 🖱️ LEFT CLICK  
   └─ Pinch: Bring Index finger and Thumb together
   └─ Small pinch gesture triggers click
   └─ Cooldown prevents accidental double-clicks

3. 📜 SCROLL MODE
   └─ All 5 fingers UP (open palm)
   └─ Move hand up → Scroll up
   └─ Move hand down → Scroll down
   └─ Natural scrolling with your whole hand

4. 🔊 VOLUME CONTROL
   └─ Thumb + Index finger UP (other fingers down)
   └─ Distance between fingers controls volume
   └─ Pinch close → Quiet
   └─ Spread apart → Loud

5. 🖱️ RIGHT CLICK
   └─ Only Pinky finger UP (all others down)
   └─ Quick right-click action

6. ✊ DRAG AND DROP
   └─ Closed fist (all fingers down)
   └─ Make a fist to hold/drag
   └─ Open hand to release

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⌨️  KEYBOARD SHORTCUTS:
  • Press 'Q' → Quit application
  • Press 'S' → Toggle statistics display

💡 TIPS FOR BEST RESULTS:
  ✓ Good lighting (webcam needs to see your hand clearly)
  ✓ Plain background (avoid busy patterns)
  ✓ Hand at center of frame
  ✓ Keep hand 1-2 feet from camera
  ✓ Palm facing camera
  ✓ Smooth, deliberate movements

⚡ PERFORMANCE:
  • Runs at 30-60 FPS on most computers
  • Low latency cursor tracking
  • No GPU required (CPU only)
  • Works with any USB webcam
    """)


def quick_start():
    """Quick start the controller"""
    print_header("QUICK START - HAND GESTURE CONTROLLER")
    
    controller = HandGestureController()
    
    print("\n📦 Checking dependencies...")
    deps = controller.check_dependencies()
    
    all_available = all(deps.values())
    
    for dep, available in deps.items():
        status = "✓ Installed" if available else "✗ Missing"
        print(f"  {dep:15} {status}")
    
    if not all_available:
        print("\n❌ Missing dependencies!")
        print(controller.get_missing_dependencies_message())
        print("\nAfter installing, run this demo again.")
        return
    
    print("\n✅ All dependencies available!")
    
    print("\n🎥 Initializing camera...")
    result = controller.initialize()
    
    if not result["success"]:
        print(f"\n❌ Initialization failed: {result['error']}")
        if 'help' in result:
            print(f"\n💡 {result['help']}")
        return
    
    print(f"✓ {result['message']}")
    print(f"✓ Screen: {result['screen_size']}")
    print(f"✓ {result['camera']}")
    
    print("\n" + "=" * 70)
    input("Press ENTER to start the hand gesture controller...")
    print("=" * 70)
    
    result = controller.start(show_video=True)
    
    print("\n" + "=" * 70)
    print("SESSION COMPLETE")
    print("=" * 70)
    
    if result["success"]:
        stats = result["stats"]
        print(f"\n📊 Statistics:")
        print(f"  Total gestures:  {stats['total_gestures']}")
        print(f"  Clicks:          {stats['clicks']}")
        print(f"  Scrolls:         {stats['scrolls']}")
        print(f"  Drags:           {stats['drags']}")
    else:
        print(f"\n❌ Error: {result['error']}")


def test_mode():
    """Test individual components"""
    print_header("TEST MODE")
    
    controller = HandGestureController()
    
    print("\n1. Testing dependencies...")
    deps = controller.check_dependencies()
    for dep, available in deps.items():
        print(f"  {dep}: {'✓' if available else '✗'}")
    
    if not all(deps.values()):
        print("\n⚠️  Some dependencies missing. Cannot proceed with tests.")
        return
    
    print("\n2. Testing camera access...")
    result = controller.initialize(camera_id=0)
    if result["success"]:
        print(f"  ✓ Camera initialized: {result['camera']}")
        print(f"  ✓ Screen size: {result['screen_size']}")
    else:
        print(f"  ✗ Failed: {result['error']}")
        return
    
    print("\n3. Testing hand detection...")
    print("  Show your hand to the camera for 5 seconds...")
    
    import time
    start_time = time.time()
    frames_with_hand = 0
    total_frames = 0
    
    while time.time() - start_time < 5:
        import cv2
        success, frame = controller.cap.read()
        if success:
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = controller.hands.process(frame_rgb)
            
            total_frames += 1
            if results.multi_hand_landmarks:
                frames_with_hand += 1
    
    detection_rate = (frames_with_hand / total_frames * 100) if total_frames > 0 else 0
    print(f"  Detection rate: {detection_rate:.1f}% ({frames_with_hand}/{total_frames} frames)")
    
    if detection_rate > 70:
        print("  ✓ Hand detection working well!")
    elif detection_rate > 30:
        print("  ⚠️  Moderate detection. Try better lighting.")
    else:
        print("  ✗ Poor detection. Check camera position and lighting.")
    
    controller.cleanup()
    print("\n✅ Test complete!")


def interactive_menu():
    """Interactive menu"""
    while True:
        print_header("HAND GESTURE MOUSE CONTROLLER - MENU")
        
        print("\n1. Quick Start (Launch Controller)")
        print("2. View Gestures Guide")
        print("3. Run System Test")
        print("4. View Example Code")
        print("0. Exit")
        
        choice = input("\nSelect option (0-4): ").strip()
        
        if choice == '0':
            print("\n👋 Goodbye!")
            break
        elif choice == '1':
            quick_start()
        elif choice == '2':
            show_gestures_guide()
        elif choice == '3':
            test_mode()
        elif choice == '4':
            show_example_code()
        else:
            print("❌ Invalid option!")


def show_example_code():
    """Show example usage code"""
    print_header("EXAMPLE CODE")
    
    print("""
📝 BASIC USAGE:

```python
from modules.automation.hand_gesture_controller import HandGestureController

# Create controller
controller = HandGestureController()

# Check dependencies
deps = controller.check_dependencies()
if not all(deps.values()):
    print(controller.get_missing_dependencies_message())
    exit()

# Initialize
result = controller.initialize(camera_id=0)
if not result["success"]:
    print(f"Error: {result['error']}")
    exit()

# Start controller (blocks until quit)
result = controller.start(show_video=True)

# Get statistics
stats = controller.get_stats()
print(f"Total gestures: {stats['total_gestures']}")
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 ADVANCED USAGE WITH CUSTOM SETTINGS:

```python
# Initialize with custom detection thresholds
result = controller.initialize(
    camera_id=0,
    detection_confidence=0.8,  # Higher = more strict
    tracking_confidence=0.8
)

# Adjust smoothing (higher = smoother but slower)
controller.smoothing = 7  # Default is 5

# Adjust click cooldown
controller.cooldown_frames = 15  # Default is 10

# Start without video display (headless mode)
result = controller.start(show_video=False)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 INTEGRATION WITH EXISTING CODE:

```python
import threading

def run_gesture_controller():
    controller = HandGestureController()
    controller.initialize()
    controller.start()

# Run in background thread
gesture_thread = threading.Thread(target=run_gesture_controller)
gesture_thread.daemon = True
gesture_thread.start()

# Your main application continues here
```
    """)


if __name__ == "__main__":
    print("\n🎮 HAND GESTURE MOUSE CONTROLLER DEMO")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--quick':
            quick_start()
        elif sys.argv[1] == '--test':
            test_mode()
        elif sys.argv[1] == '--guide':
            show_gestures_guide()
        else:
            print("Usage:")
            print("  python demo_hand_gesture_controller.py           # Interactive menu")
            print("  python demo_hand_gesture_controller.py --quick   # Quick start")
            print("  python demo_hand_gesture_controller.py --test    # Run tests")
            print("  python demo_hand_gesture_controller.py --guide   # View guide")
    else:
        interactive_menu()
