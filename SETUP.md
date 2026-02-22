# 📦 Models & Data Setup Guide

## Directory Structure

Your `plant-health-guardian/` folder should look like:

```
plant-health-guardian/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── models/
│   ├── best_model.pth              ← Your trained model weights
│   ├── final_model.pth             ← Final epoch weights (backup)
│   ├── training_history.json       ← Training metrics & loss curves
│   └── config.json                 ← Model configuration
└── data/
    └── label_mapping.json          ← Class names & IDs mapping
```

## 📥 How to Get the Model Files

The model files come from your training in Google Colab. They're stored in `/content/plant_model_output/`.

### Option 1: Download from Colab (Recommended)

1. In Google Colab, go to the file explorer on the left
2. Navigate to `/content/plant_model_output/`
3. Right-click on each file and download:
   - `best_model.pth`
   - `final_model.pth`
   - `training_history.json`
   - `config.json`

4. Create folders in your VS Code project:
   ```
   models/
   data/
   ```

5. Place downloaded files:
   ```
   models/best_model.pth
   models/final_model.pth
   models/training_history.json
   models/config.json
   ```

### Option 2: Copy from Colab (Alternative)

In Colab, run:
```python
# Zip your model files
!cd /content && zip -r plant_model.zip plant_model_output/

# Download the zip
from google.colab import files
files.download('/content/plant_model.zip')

# Extract locally and move files to your project
```

## 🏷️ Label Mapping File

You also need the `label_mapping.json` from your preprocessing step in Colab:

1. In Colab file explorer, go to `/content/plant_dataset/`
2. Download `label_mapping.json`
3. Create a `data/` folder in your project
4. Place the file: `data/label_mapping.json`

This file contains the mapping of:
- Class index → Disease name
- Example:
  ```json
  {
    "label2id": {
      "Apple___Apple_scab": 0,
      "Apple___Black_rot": 1,
      ...
      "Tomato___healthy": 39
    },
    "id2label": {
      "0": "Apple___Apple_scab",
      "1": "Apple___Black_rot",
      ...
      "39": "Tomato___healthy"
    }
  }
  ```

## ✅ Verification Checklist

After copying all files, verify your structure:

```bash
# In terminal, run from project root:
ls -la models/
# Should show:
# - best_model.pth (should be ~350MB)
# - final_model.pth
# - training_history.json
# - config.json

ls -la data/
# Should show:
# - label_mapping.json
```

## 🚀 Ready to Run!

Once all files are in place, you can run:

```bash
streamlit run app.py
```

---

## 📊 Model File Sizes

- `best_model.pth` - ~350-370 MB (contains all model weights)
- `final_model.pth` - ~350-370 MB (backup)
- `label_mapping.json` - ~2-3 KB (tiny!)
- `config.json` - ~1 KB (tiny!)
- `training_history.json` - ~5-10 KB (metrics from training)

**Total:** ~700 MB for your project (mostly model weights)

---

## 🔧 Troubleshooting

### "FileNotFoundError: models/best_model.pth"
- Check that `best_model.pth` exists in the `models/` folder
- Path should be: `plant-health-guardian/models/best_model.pth`

### "FileNotFoundError: data/label_mapping.json"
- Check that `label_mapping.json` exists in the `data/` folder
- Path should be: `plant-health-guardian/data/label_mapping.json`

### Model file is empty/corrupted
- Re-download from Colab
- Check file size (~350 MB for best_model.pth)
- If small (<1 MB), download failed—try again

---

## 📝 Notes

- The model files are **essential** for the app to work
- Don't modify the file structure or names
- Keep both `best_model.pth` and `final_model.pth` as backups
- The label mapping must match your trained model's classes

---

**Ready? Download the files and start the app!** 🚀
