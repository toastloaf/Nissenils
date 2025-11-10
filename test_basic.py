#!/usr/bin/env python3
"""
Basic test script to verify the setup without requiring a webcam
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    required_packages = [
        ('cv2', 'opencv-python'),
        ('torch', 'torch'),
        ('transformers', 'transformers'),
        ('PIL', 'Pillow'),
        ('numpy', 'numpy'),
    ]
    
    optional_packages = [
        ('sounddevice', 'sounddevice'),
        ('soundfile', 'soundfile'),
    ]
    
    failed = []
    
    # Test required packages
    for module_name, package_name in required_packages:
        try:
            importlib.import_module(module_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} (REQUIRED)")
            failed.append(package_name)
    
    # Test optional packages
    for module_name, package_name in optional_packages:
        try:
            importlib.import_module(module_name)
            print(f"  ✓ {package_name} (optional)")
        except ImportError:
            print(f"  ⚠ {package_name} (optional - audio will be disabled)")
    
    return len(failed) == 0

def test_torch():
    """Test PyTorch and CUDA availability"""
    print("\nTesting PyTorch...")
    try:
        import torch
        print(f"  ✓ PyTorch version: {torch.__version__}")
        print(f"  ✓ CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  ✓ CUDA version: {torch.version.cuda}")
            print(f"  ✓ GPU device: {torch.cuda.get_device_name(0)}")
        else:
            print("  ℹ Running on CPU (GPU recommended for best performance)")
        return True
    except Exception as e:
        print(f"  ✗ PyTorch test failed: {e}")
        return False

def test_transformers():
    """Test transformers library"""
    print("\nTesting transformers...")
    try:
        import transformers
        print(f"  ✓ Transformers version: {transformers.__version__}")
        return True
    except Exception as e:
        print(f"  ✗ Transformers test failed: {e}")
        return False

def test_opencv():
    """Test OpenCV"""
    print("\nTesting OpenCV...")
    try:
        import cv2
        print(f"  ✓ OpenCV version: {cv2.__version__}")
        return True
    except Exception as e:
        print(f"  ✗ OpenCV test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 Real-time Object Roleplay AI - Basic Tests")
    print("="*60)
    print()
    
    all_pass = True
    
    # Run tests
    all_pass = test_imports() and all_pass
    all_pass = test_torch() and all_pass
    all_pass = test_transformers() and all_pass
    all_pass = test_opencv() and all_pass
    
    print("\n" + "="*60)
    if all_pass:
        print("✅ All tests passed!")
        print("\nYou can now run the main application:")
        print("  python3 object_roleplay.py")
    else:
        print("❌ Some tests failed")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
    print("="*60)
    
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
