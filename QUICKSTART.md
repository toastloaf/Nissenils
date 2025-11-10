# 🚀 Quick Start Guide

Get up and running with the Object Roleplay AI in 5 minutes!

## Prerequisites

- Python 3.8+
- Webcam
- 2GB+ free disk space (for models)
- Internet connection (first run only)

## Installation (3 steps)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Or use the setup script (Linux/Mac):**
```bash
./setup.sh
```

### 2. Test Your Setup (Optional but Recommended)

```bash
python3 test_basic.py
```

This will verify all dependencies are installed correctly.

### 3. Run the Application

```bash
python3 object_roleplay.py
```

**First run**: Models will be downloaded automatically (~500MB-1GB). This takes 2-5 minutes depending on your internet speed.

**Subsequent runs**: Start instantly using cached models.

## 🎮 Using the Application

1. **Allow camera access** when prompted
2. **Point your webcam** at different objects:
   - Your face
   - A cup or mug
   - Your phone
   - A book
   - A plant
   - Any other object!
3. **Wait 3 seconds** for detection
4. **Watch the AI roleplay** as that object!
5. **Try different objects** for different personalities
6. **Press 'q' or ESC** to exit

## 💡 Tips

- **Good lighting** = better object detection
- **Clear, centered objects** work best
- **Wait a few seconds** between switching objects
- **Try yourself!** The AI can roleplay as a person too

## ⚠️ Troubleshooting

### "Camera not found"
- Check if your webcam is connected
- Close other apps using the camera (Zoom, Skype, etc.)
- Try unplugging and reconnecting your webcam

### "Out of memory"
- Close other applications
- The models will automatically use CPU if GPU isn't available

### "Import errors"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Models downloading slowly
- Be patient on first run
- Ensure stable internet connection
- Models are cached locally after first download

## 🎯 What to Expect

On first run:
```
🤖 Initializing Object Roleplay AI...
📹 Loading vision model (FastVLM-0.5B)...
   Using device: cuda
   ✓ Vision model loaded successfully
🔊 Loading TTS model (neutts-air)...
   Note: neutts-air TTS requires special setup
   Using text display for now
📷 Starting webcam...
   ✓ Webcam started successfully

====================================================
🎭 Object Roleplay AI is now running!
====================================================
📹 Point your camera at different objects
🤖 The AI will roleplay as whatever it sees
👋 Press 'q' to quit
====================================================

🔍 Analyzing frame...
✨ New object detected: coffee mug
🗣️  'I'm a mug! I love holding hot beverages!'
```

## 🎨 Customization

Want to add your own object personalities? Edit `object_roleplay.py`:

```python
self.personality_templates = {
    "your_object": [
        "Custom personality line 1",
        "Custom personality line 2",
    ],
}
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed information
- Check out the [models on HuggingFace](https://huggingface.co/):
  - [FastVLM-0.5B](https://huggingface.co/apple/FastVLM-0.5B)
  - [neutts-air](https://huggingface.co/neuphonic/neutts-air)
- Customize object personalities
- Share your experience!

## 🆘 Need Help?

If you encounter issues:
1. Run `python3 test_basic.py` to diagnose problems
2. Check the full README for troubleshooting
3. Ensure all prerequisites are met
4. Try reinstalling dependencies

---

**Enjoy your object roleplay experience! 🎭**
