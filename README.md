# 🎭 Real-time Object Roleplay AI

An AI-powered application that uses your webcam to identify objects in real-time and roleplays as them with personality and voice! Point your camera at anything - a cup, a phone, a person, or even yourself - and watch as the AI embodies that object with character and charm.

## ✨ Features

- 🎥 **Real-time Object Detection**: Uses Apple's FastVLM-0.5B vision model to identify objects in your webcam feed
- 🎭 **Dynamic Roleplay**: AI generates personality-driven dialogue as the detected object
- 🔊 **Voice Output**: Text-to-speech using Neuphonic's neutts-air model (framework ready)
- 🖼️ **Live Preview**: See yourself and the AI's interpretation in real-time
- ⚡ **Optimized Performance**: Efficient processing for smooth real-time experience

## 🤖 AI Models

This project uses two state-of-the-art AI models:

1. **[Apple FastVLM-0.5B](https://huggingface.co/apple/FastVLM-0.5B)**: A fast vision-language model for object detection
2. **[Neuphonic NeuTTS Air](https://huggingface.co/neuphonic/neutts-air)**: High-quality text-to-speech model

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam
- CUDA-capable GPU (optional, but recommended for better performance)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python object_roleplay.py
   ```

## 📖 Usage

1. **Start the program**: Run `python object_roleplay.py`
2. **Position your webcam**: Point it at different objects or yourself
3. **Watch the magic**: The AI will detect objects every few seconds and roleplay as them
4. **Interactive Fun**: Try different objects to see unique personalities!
5. **Exit**: Press 'q' or ESC to quit

## 🎯 How It Works

1. **Capture**: The program continuously captures frames from your webcam
2. **Detect**: Every 3 seconds, FastVLM analyzes the frame to identify the main object
3. **Roleplay**: When a new object is detected, the AI generates personality-driven dialogue
4. **Speak**: The text is converted to speech using TTS (displayed as text for now)
5. **Display**: Everything is shown in a clean real-time interface

## 🎨 Object Personalities

The AI has unique personalities for different objects:

- **Cup**: "I'm a cup! I love holding liquids!"
- **Phone**: "Beep boop! I'm your trusty phone!"
- **Book**: "I'm a book full of knowledge!"
- **Person**: "Hi! I'm a person just like you!"
- **And many more!**

## ⚙️ Configuration

You can customize the behavior by modifying these parameters in `object_roleplay.py`:

- `detection_interval`: Time between object detections (default: 3 seconds)
- `personality_templates`: Add your own object personalities
- Camera resolution: Adjust in `start_webcam()` method

## 🛠️ Troubleshooting

### Webcam Issues
- **Camera not found**: Make sure your webcam is connected and not used by another application
- **Permission denied**: Grant camera permissions to your terminal/Python

### Model Loading Issues
- **Out of memory**: Try using CPU instead of GPU, or reduce image resolution
- **Model download fails**: Check your internet connection and HuggingFace access

### Performance Issues
- **Laggy video**: Increase `detection_interval` to reduce processing frequency
- **Slow detection**: Use a GPU for better performance
- **High CPU usage**: Consider reducing camera resolution

## 🔧 Advanced Setup

### GPU Acceleration
If you have an NVIDIA GPU with CUDA:
```bash
# Install PyTorch with CUDA support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Audio Output (TTS)
To enable full audio output with neutts-air:
1. Ensure `sounddevice` and `soundfile` are installed
2. The TTS model integration is prepared in the code
3. Check Neuphonic's documentation for specific setup requirements

## 📝 Technical Details

### Architecture
- **Vision Pipeline**: FastVLM-0.5B processes webcam frames
- **Text Generation**: Template-based roleplay with personality traits
- **Audio Pipeline**: Text-to-speech conversion (framework ready)
- **UI Layer**: OpenCV-based real-time display

### Performance
- Frame processing: ~30 FPS display
- Object detection: Every 3 seconds (configurable)
- Model loading: ~5-10 seconds on first run
- Memory usage: ~2-4GB with GPU, ~1-2GB with CPU

## 🤝 Contributing

Feel free to contribute! Some ideas:
- Add more object personalities
- Improve object detection accuracy
- Add gesture recognition
- Create different roleplay modes
- Enhance the UI

## 📄 License

This project uses models from HuggingFace. Please refer to their respective licenses:
- [FastVLM License](https://huggingface.co/apple/FastVLM-0.5B)
- [NeuTTS License](https://huggingface.co/neuphonic/neutts-air)

## 🙏 Acknowledgments

- Apple for FastVLM-0.5B
- Neuphonic for neutts-air
- HuggingFace for model hosting
- The open-source community

## 🎮 Fun Use Cases

- **Education**: Learn about objects around you
- **Entertainment**: Create funny videos with object personalities
- **Accessibility**: Voice feedback for object recognition
- **Creative Projects**: Interactive installations and performances
- **Kids**: Educational and entertaining for children

---

Made with ❤️ and AI

**Note**: This is an experimental project combining cutting-edge AI models. Performance may vary based on your hardware and internet connection.
