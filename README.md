# 🌿 Plant Health Guardian

**AI-powered plant disease detection to keep your green friends thriving**

An intelligent app that uses a fine-tuned Swin Transformer neural network to identify plant diseases from photos and provide personalized care recommendations.

---

## 🎯 Project Overview

This project won a hackathon by combining:
- **99.87% accurate** disease classification model
- **40 plant disease types** with detailed care recommendations
- **Streamlit web interface** for easy user interaction
- **Personal motivation story** (basil-inspired!)

**Model Details:**
- Architecture: Swin Transformer (microsoft/swin-base-patch4-window7-224)
- Training Data: 66,305 plant leaf images (70% train, 15% val, 15% test)
- Training Time: ~2 hours on L4 GPU
- Test Accuracy: **99.87%**

---

Uploading Screen Recording 2026-02-22 at 11.39.56 AM.mov…



## 📁 Project Structure

```
plant-health-guardian/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── data/
│   └── label_mapping.json         # Class label mappings
├── models/
│   ├── best_model.pth             # Trained Swin model weights
│   ├── final_model.pth            # Final epoch weights
│   ├── training_history.json      # Training metrics
│   └── config.json                # Training configuration
├── README.md                       # This file
└── .gitignore                      # Git ignore rules
```

---

## 🚀 Quick Start

### 1. Clone/Download the Project
```bash
cd plant-health-guardian
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📸 How to Use

1. **Open the app** in your browser
2. **Upload a plant photo**
   - Clear photo of a leaf or affected area
   - JPG or PNG format
   - Good lighting for best results
3. **Get instant analysis**
   - Top 5 disease predictions with confidence scores
   - Detailed disease information
   - Specific care recommendations
4. **Follow the care tips** to save your plant! 💚

---

## 🧠 Model Details

### Architecture
- **Base Model:** Swin Transformer (Pre-trained on ImageNet)
- **Classification Head:** Fine-tuned for 40 plant disease classes
- **Input Size:** 224×224 RGB images
- **Optimizer:** AdamW with learning rate scheduling
- **Loss:** Cross-Entropy Loss

### Training Process
- **Dataset:** PlantVillage + custom basil data
- **Data Augmentation:** 
  - Random flips (H, V)
  - Random rotations (±20°)
  - Color jitter
  - Random affine transformations
- **Epochs:** 5
- **Batch Size:** 32
- **Learning Rate:** 1e-4 (with cosine annealing)
- **Hardware:** L4 GPU (Google Colab)

### Performance
- **Test Accuracy:** 99.87%
- **Val Accuracy:** 99.88%
- **Inference Time:** ~1-2 seconds per image

---

## 🌿 Supported Plant Diseases

The model can identify diseases for these plant types:
- Apple (3 diseases)
- Basil (2 conditions: healthy, unhealthy) ⭐
- Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato

**Total:** 40 plant-disease combinations

---

## 💡 Special Features

### 🌱 Basil Focus
This app was built with personal motivation—to help people save their failing basil plants! If your basil needs help, the app provides extra detailed care instructions specifically designed to bring it back to health.

### 📊 Confidence Visualization
Visual confidence bars show model certainty for top 5 predictions, helping users understand reliability.

### 🎯 Disease-Specific Care
Each disease includes:
- Detailed description
- Common symptoms
- Step-by-step treatment recommendations
- Prevention tips

---

## 🛠️ Development & Training

### To Re-train the Model (Advanced)

If you want to train the model yourself:

1. **Prepare Dataset:**
   ```bash
   python preprocessing/prepare_data.py
   ```

2. **Train Model:**
   ```bash
   python training/train_swin.py
   ```

3. **Evaluate:**
   ```bash
   python evaluation/test_model.py
   ```

(Scripts available upon request)

---

## 📦 Dependencies

- **streamlit** - Web app framework
- **torch** - Deep learning framework
- **torchvision** - Computer vision utilities
- **transformers** - Pre-trained models (HuggingFace)
- **Pillow** - Image processing
- **numpy** - Numerical computing

See `requirements.txt` for exact versions.

---

## 🐛 Troubleshooting

### "Model not found" error
- Ensure `models/best_model.pth` exists in the project directory
- Check file path in `app.py` line 222

### "Label mapping not found" error
- Ensure `data/label_mapping.json` exists
- Check file path in `app.py` line 232

### Slow inference on CPU
- Model is optimized for GPU
- CPU inference takes 10-20 seconds (normal)
- Consider using GPU for faster results

### Out of memory error
- Reduce batch size in model loading
- Use GPU instead of CPU if available

---

## 📈 Model Metrics

| Metric | Value |
|--------|-------|
| Test Accuracy | 99.87% |
| Validation Accuracy | 99.88% |
| Total Parameters | 87.7M |
| Trainable Parameters | 1.23M |
| Inference Time (GPU) | 1-2 sec |
| Inference Time (CPU) | 10-20 sec |

---

## 🎓 How It Was Built

This project was created for a UC Berkeley hackathon. The development process:

1. **Data Selection** - Chose PlantVillage dataset + custom basil data
2. **Preprocessing** - Organized 66K images into train/val/test splits
3. **Model Selection** - Fine-tuned Swin Transformer for plant disease classification
4. **Training** - Achieved 99.87% accuracy in 2 hours on L4 GPU
5. **Interface** - Built Streamlit app for easy user interaction
6. **Deployment** - Created production-ready project structure

---

## 💚 Inspiration

This app was born from a personal story: trying to grow basil in a dorm room and watching it slowly die without understanding why. The goal is to help other plant lovers diagnose and save their plants before it's too late.

Every plant deserves a chance! 🌱

---

## 📝 License

This project is open source and available for educational and personal use.

---

## 🤝 Contributing

Suggestions for improvements? Feel free to:
- Report bugs or issues
- Suggest new plant types to add
- Improve care recommendations
- Enhance the UI/UX

---

## 👨‍💻 Author

Built with ❤️ for plant lovers everywhere.

**Contact/Questions:** Feel free to reach out!

---

## 🎉 Acknowledgments

- **Dataset:** PlantVillage dataset (54,000+ images)
- **Model:** Microsoft Swin Transformer
- **Framework:** Streamlit for the beautiful web interface
- **Inspiration:** Every plant that deserves a second chance

---

## 📞 Support

Having issues? Try:
1. Check that all dependencies are installed: `pip install -r requirements.txt`
2. Ensure model files are in the correct directories
3. Try running with `streamlit run app.py --logger.level=debug` for more info
4. Check console output for error messages

---

**Happy gardening! 🌿🎋🌱**
