#!/usr/bin/env python3
"""
Web-Based Face Recognition Test
Works on Windows - shows camera feed in browser
"""

import streamlit as st
import cv2
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

from modules.automation.face_trainer import FaceRecognizer


def main():
    st.set_page_config(page_title="VATSAL AI - Face Recognition", layout="wide")
    
    st.title("🎥 VATSAL AI - Face Recognition Test")
    st.markdown("---")
    
    # Load model
    model_path = "biometric_data/faces/models/face_model.yml"
    
    if not os.path.exists(model_path):
        st.error("❌ Model not found!")
        st.info("💡 Train the model first: `python train_vatsal_face.py`")
        return
    
    # Initialize recognizer
    @st.cache_resource
    def load_recognizer():
        recognizer = FaceRecognizer(model_path)
        if recognizer.load_model():
            return recognizer
        return None
    
    recognizer = load_recognizer()
    
    if recognizer is None:
        st.error("❌ Failed to load model!")
        return
    
    st.success(f"✅ Model loaded! Can recognize: {list(recognizer.labels.keys())}")
    
    # Camera controls
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("### Controls")
        run_camera = st.checkbox("📹 Start Camera", value=True)
        show_confidence = st.checkbox("Show Confidence", value=True)
        confidence_threshold = st.slider("Min Confidence %", 0, 100, 50)
    
    with col1:
        st.markdown("### Live Camera Feed")
        camera_placeholder = st.empty()
    
    # Stats
    stats_placeholder = st.empty()
    
    if run_camera:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("❌ Could not open camera!")
            return
        
        recognition_count = {}
        frame_count = 0
        
        stop_button = st.button("⏹️ Stop Camera")
        
        while run_camera and not stop_button:
            ret, frame = cap.read()
            
            if not ret:
                st.error("❌ Failed to read from camera")
                break
            
            frame_count += 1
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = recognizer.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )
            
            # Recognize each face
            for (x, y, w, h) in faces:
                name, confidence = recognizer.recognize_face(gray, (x, y, w, h))
                
                # Track recognition
                if confidence > confidence_threshold:
                    recognition_count[name] = recognition_count.get(name, 0) + 1
                
                # Choose color based on confidence
                if confidence > 70:
                    color = (0, 255, 0)  # Green - excellent
                    status = "✅ Excellent"
                elif confidence > 50:
                    color = (0, 255, 255)  # Yellow - good
                    status = "👍 Good"
                else:
                    color = (0, 165, 255)  # Orange - poor
                    status = "⚠️ Poor"
                
                # Draw rectangle
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                
                # Draw name
                label = f"{name.upper()}"
                if show_confidence:
                    label += f" ({confidence:.1f}%)"
                
                cv2.putText(
                    frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2
                )
                
                # Draw status
                cv2.putText(
                    frame, status, (x, y + h + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
                )
            
            # Add info overlay
            info_text = f"Faces Detected: {len(faces)} | Frame: {frame_count}"
            cv2.putText(
                frame, info_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
            )
            
            # Convert BGR to RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Display frame
            camera_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
            
            # Update stats
            if recognition_count:
                stats_md = "### 📊 Recognition Stats\n\n"
                for name, count in recognition_count.items():
                    stats_md += f"- **{name.upper()}**: {count} times\n"
                stats_placeholder.markdown(stats_md)
            
            # Small delay
            if frame_count % 30 == 0:
                st.rerun()
        
        cap.release()
    else:
        st.info("📹 Click 'Start Camera' to begin face recognition")


if __name__ == "__main__":
    main()
