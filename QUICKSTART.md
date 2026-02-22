# ⚡ Quick Start Guide

Get **Plant Health Guardian** running in 5 minutes!

---

## 📥 Step 1: Download Model Files from Colab

Your trained model is in Google Colab. You need to download it:

1. **Open your Colab notebook** where you trained the model
2. **Open Files panel** (folder icon on the left)
3. **Navigate to:** `/content/plant_model_output/`
4. **Download these files:**
   - `best_model.pth` (the important one!)
   - `final_model.pth` (backup)
   - `training_history.json`
   - `config.json`

5. **Also download label mapping:**
   - Navigate to `/content/plant_dataset/`
   - Download `label_mapping.json`

---

## 💾 Step 2: Set Up Project Structure

Create this folder structure in your project:

```
plant-health-guardian/
├── models/
│   ├── best_model.pth          ← Paste the file here
│   ├── final_model.pth
│   ├── training_history.json
│   └── config.json
└── data/
    └── label_mapping.json      ← Paste the file here
```

---

## 🚀 Step 3: Run the App

### **Option A: Automatic (Easiest)**

**On Windows:**
```bash
run.bat
```

**On macOS/Linux:**
```bash
bash run.sh
```

This will automatically:
- Create virtual environment
- Install dependencies
- Start the app

### **Option B: Manual**

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

---

## 🌐 Step 4: Use the App

1. **Browser opens automatically** to `http://localhost:8501`
2. **Upload a plant photo**
3. **Get instant disease prediction**
4. **Read care recommendations**

That's it! 🎉

---

## ✅ Verification Checklist

Before running, make sure you have:

- [ ] `models/best_model.pth` exists (~350 MB)
- [ ] `data/label_mapping.json` exists (~2 KB)
- [ ] Python 3.8+ installed
- [ ] All files from "Step 2" in correct locations

---

## 🔧 Troubleshooting

### App won't start - "Model not found"
```
Solution: Check that models/best_model.pth exists
Run: ls models/  (or dir models\ on Windows)
```

### "ModuleNotFoundError: No module named 'streamlit'"
```
Solution: Install dependencies
Run: pip install -r requirements.txt
```

### Port 8501 already in use
```
Solution: Run on different port
Command: streamlit run app.py --server.port 8502
```

### "best_model.pth is empty or corrupted"
```
Solution: Re-download from Colab
- The file should be ~350 MB
- If it's smaller, download failed
```

---

## 📊 What Should Happen

When you run the app:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  Edit app.py and save to update! ✨
```

Then your browser opens to a beautiful app with:
- 🌿 Plant Health Guardian header
- 📸 Image upload area
- 💡 Instructions
- 📊 Prediction results
- 💚 Care recommendations

---

## 🎯 Next Steps

Once running, you can:

1. **Test with plant photos** - Try your camera roll
2. **Identify your plant** - See what disease it might have
3. **Get care tips** - Follow recommendations to save your plant
4. **Share with others** - Show friends your AI plant doctor!

---

## 📞 Still Having Issues?

1. **Check SETUP.md** - Detailed setup guide
2. **Check README.md** - Full documentation
3. **Common issues:**
   - Missing model file → Download from Colab
   - Missing label mapping → Download from Colab
   - Dependencies not installed → `pip install -r requirements.txt`

---

**You're all set! Happy plant detecting! 🌱**
