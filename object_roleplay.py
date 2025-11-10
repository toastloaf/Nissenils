#!/usr/bin/env python3
"""
Real-time Object Roleplay AI
Uses webcam to identify objects and roleplays as them with voice output.
"""

import cv2
import torch
import numpy as np
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import threading
import queue
import time
import random
import warnings
import sys
import os

warnings.filterwarnings('ignore')

# Try importing TTS libraries
try:
    import sounddevice as sd
    import soundfile as sf
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Warning: sounddevice not available. Audio output will be disabled.")

try:
    from transformers import pipeline
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


class ObjectRoleplayAI:
    def __init__(self):
        print("🤖 Initializing Object Roleplay AI...")
        
        # Initialize vision model (FastVLM)
        print("📹 Loading vision model (FastVLM-0.5B)...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"   Using device: {self.device}")
        
        try:
            self.processor = AutoProcessor.from_pretrained(
                "apple/FastVLM-0.5B",
                trust_remote_code=True
            )
            self.model = AutoModelForVision2Seq.from_pretrained(
                "apple/FastVLM-0.5B",
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            print("   ✓ Vision model loaded successfully")
        except Exception as e:
            print(f"   ✗ Error loading vision model: {e}")
            print("   Falling back to basic object detection...")
            self.model = None
            self.processor = None
        
        # Initialize TTS
        print("🔊 Loading TTS model (neutts-air)...")
        self.tts_available = False
        if TTS_AVAILABLE:
            try:
                # Try to load the TTS model
                # Note: neuphonic/neutts-air might require special handling
                # For now, we'll use a fallback TTS if needed
                self.tts_pipe = None
                print("   Note: neutts-air TTS requires special setup")
                print("   Using text display for now")
            except Exception as e:
                print(f"   Could not load TTS: {e}")
        
        # State management
        self.current_object = None
        self.last_detection_time = 0
        self.detection_interval = 3.0  # Analyze every 3 seconds
        self.roleplay_queue = queue.Queue()
        self.running = True
        
        # Webcam
        self.cap = None
        
        # Roleplay personality traits for different objects
        self.personality_templates = {
            "default": [
                "Oh hello there! I'm {object}!",
                "Hey! Did you notice me? I'm {object}!",
                "Greetings! I'm a {object}, pleased to meet you!",
                "Hi! I'm just here being a {object}!",
            ],
            "person": [
                "Hi! I'm a person just like you!",
                "Hello! I see you're looking at me!",
                "Hey there! I'm a human being!",
            ],
            "cup": [
                "I'm a cup! I love holding liquids!",
                "Hey! I'm a cup. Fill me up!",
                "I'm a cup, and I'm feeling a bit empty...",
            ],
            "phone": [
                "I'm a phone! Call someone!",
                "Beep boop! I'm your trusty phone!",
                "I'm a phone, connecting people since... well, recently!",
            ],
            "book": [
                "I'm a book full of knowledge!",
                "Read me! I'm a book!",
                "I'm a book. I contain stories and wisdom!",
            ],
            "keyboard": [
                "I'm a keyboard! Type on me!",
                "Click clack! I'm a keyboard!",
                "I help you write! I'm a keyboard!",
            ],
            "mouse": [
                "I'm a mouse! Click click!",
                "I help you navigate! I'm a computer mouse!",
                "Point and click with me!",
            ],
            "bottle": [
                "I'm a bottle! I hold beverages!",
                "Hey! I'm a bottle, keeper of liquids!",
                "I'm a bottle. Stay hydrated!",
            ],
            "laptop": [
                "I'm a laptop! I compute things!",
                "Beep boop! I'm your portable computer!",
                "I'm a laptop, ready to work!",
            ],
            "chair": [
                "I'm a chair! Sit on me!",
                "Hey! I'm a chair, here to support you!",
                "I'm a chair. I love being sat on!",
            ],
            "plant": [
                "I'm a plant! I need sunlight and water!",
                "Hello! I'm a plant doing photosynthesis!",
                "I'm a plant. I make oxygen for you!",
            ],
        }
    
    def start_webcam(self):
        """Initialize webcam capture"""
        print("📷 Starting webcam...")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("   ✗ Error: Could not open webcam")
            return False
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        print("   ✓ Webcam started successfully")
        return True
    
    def detect_object(self, frame):
        """Detect objects in the frame using FastVLM"""
        if self.model is None or self.processor is None:
            return "unknown object"
        
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            
            # Prepare prompt for vision model
            prompt = "What is the main object or person visible in this image? Answer with just the object name in 1-3 words."
            
            # Process the image
            inputs = self.processor(
                text=prompt,
                images=pil_image,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate detection
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=20,
                    do_sample=False
                )
            
            # Decode the output
            result = self.processor.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the object name (remove the prompt)
            if prompt in result:
                result = result.replace(prompt, "").strip()
            
            # Clean up the result
            result = result.lower().strip()
            if not result or len(result) < 2:
                result = "mysterious object"
            
            return result
            
        except Exception as e:
            print(f"   Detection error: {e}")
            return "unknown object"
    
    def generate_roleplay_text(self, object_name):
        """Generate roleplay text based on detected object"""
        # Check if we have specific templates for this object
        object_key = object_name.lower()
        
        # Find matching template
        templates = None
        for key in self.personality_templates:
            if key in object_key or object_key in key:
                templates = self.personality_templates[key]
                break
        
        if templates is None:
            templates = self.personality_templates["default"]
        
        # Select a random template and format it
        template = random.choice(templates)
        text = template.format(object=object_name)
        
        return text
    
    def speak_text(self, text):
        """Convert text to speech and play it"""
        # For now, just print the text
        # In a full implementation, this would use the TTS model
        print(f"🗣️  '{text}'")
        
        # Placeholder for TTS implementation
        # if self.tts_available and AUDIO_AVAILABLE:
        #     try:
        #         # Generate audio using neutts-air
        #         # audio = self.tts_pipe(text)
        #         # Play audio
        #         pass
        #     except Exception as e:
        #         print(f"TTS error: {e}")
    
    def process_frame(self, frame):
        """Process a frame and update detection"""
        current_time = time.time()
        
        # Only detect periodically to maintain real-time performance
        if current_time - self.last_detection_time >= self.detection_interval:
            self.last_detection_time = current_time
            
            # Detect object in frame
            print("🔍 Analyzing frame...")
            detected_object = self.detect_object(frame)
            
            # If object changed, generate new roleplay
            if detected_object != self.current_object:
                self.current_object = detected_object
                print(f"✨ New object detected: {detected_object}")
                
                # Generate and speak roleplay text
                roleplay_text = self.generate_roleplay_text(detected_object)
                self.speak_text(roleplay_text)
        
        return frame
    
    def draw_ui(self, frame):
        """Draw UI elements on the frame"""
        # Create a copy to draw on
        display_frame = frame.copy()
        
        # Draw semi-transparent overlay at the bottom
        overlay = display_frame.copy()
        height, width = display_frame.shape[:2]
        cv2.rectangle(overlay, (0, height-80), (width, height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, display_frame, 0.4, 0, display_frame)
        
        # Draw text
        if self.current_object:
            text = f"I am: {self.current_object.upper()}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(display_frame, text, (10, height-45), 
                       font, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
            
            # Draw status
            status = "🎭 Roleplaying..."
            cv2.putText(display_frame, status, (10, height-15), 
                       font, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            text = "Detecting objects..."
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(display_frame, text, (10, height-30), 
                       font, 0.7, (128, 128, 128), 2, cv2.LINE_AA)
        
        # Draw title at top
        title_overlay = display_frame.copy()
        cv2.rectangle(title_overlay, (0, 0), (width, 40), (0, 0, 0), -1)
        cv2.addWeighted(title_overlay, 0.6, display_frame, 0.4, 0, display_frame)
        cv2.putText(display_frame, "Object Roleplay AI", (10, 28), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        
        return display_frame
    
    def run(self):
        """Main loop"""
        if not self.start_webcam():
            return
        
        print("\n" + "="*60)
        print("🎭 Object Roleplay AI is now running!")
        print("="*60)
        print("📹 Point your camera at different objects")
        print("🤖 The AI will roleplay as whatever it sees")
        print("👋 Press 'q' to quit")
        print("="*60 + "\n")
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error reading frame")
                    break
                
                # Process frame for object detection
                processed_frame = self.process_frame(frame)
                
                # Draw UI
                display_frame = self.draw_ui(processed_frame)
                
                # Display the frame
                cv2.imshow('Object Roleplay AI', display_frame)
                
                # Check for quit
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # q or ESC
                    print("\n👋 Shutting down...")
                    break
                
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("✓ Cleanup complete")


def main():
    """Entry point"""
    print("\n" + "="*60)
    print("🎭 Real-time Object Roleplay AI")
    print("="*60)
    print("Models:")
    print("  • Vision: apple/FastVLM-0.5B")
    print("  • TTS: neuphonic/neutts-air")
    print("="*60 + "\n")
    
    # Create and run the AI
    ai = ObjectRoleplayAI()
    ai.run()


if __name__ == "__main__":
    main()
