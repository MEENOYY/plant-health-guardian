import streamlit as st
import torch
import json
import os
from PIL import Image
import numpy as np
from transformers import AutoImageProcessor, AutoModelForImageClassification
from datetime import datetime

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="🌿 Plant Health Guardian",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2d5016;
        margin-bottom: 30px;
    }
    .disease-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .healthy-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .care-tip {
        background-color: #f0f7ff;
        border-left: 4px solid #2d5016;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .confidence-bar {
        background-color: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin: 5px 0;
    }
    .confidence-fill {
        background: linear-gradient(90deg, #84fab0 0%, #8fd3f4 100%);
        height: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DISEASE INFORMATION DATABASE
# ============================================

DISEASE_INFO = {
    "Apple___Apple_scab": {
        "name": "Apple Scab",
        "description": "Fungal disease causing dark, scaly lesions on leaves and fruit",
        "symptoms": ["Dark, circular lesions on leaves", "Yellowing around infected areas", "Premature leaf drop"],
        "care": ["Remove infected leaves immediately", "Ensure good air circulation", "Apply fungicide if needed", "Keep leaves dry"]
    },
    "Apple___Black_rot": {
        "name": "Apple Black Rot",
        "description": "Serious fungal disease causing rot on fruit and cankers on branches",
        "symptoms": ["Large, dark, circular lesions", "Concentric rings on fruit", "Cankers on branches"],
        "care": ["Prune infected branches", "Remove fallen fruit", "Apply fungicide in spring", "Improve drainage"]
    },
    "Apple___Cedar_apple_rust": {
        "name": "Cedar Apple Rust",
        "description": "Fungal disease that alternates between apple and cedar trees",
        "symptoms": ["Yellow spots on leaves", "Orange gelatinous horns on cedar", "Premature leaf drop"],
        "care": ["Remove nearby cedar trees if possible", "Apply preventive fungicide", "Improve air circulation", "Prune dense branches"]
    },
    "Apple___healthy": {
        "name": "Healthy Apple Leaf",
        "description": "Your apple leaf looks great! Keep up the good care.",
        "symptoms": ["No visible disease", "Normal coloration", "Firm texture"],
        "care": ["Continue regular watering", "Monitor for new issues", "Maintain good nutrition", "Regular pruning"]
    },
    "Basil___healthy": {
        "name": "✨ Healthy Basil (Your Little Green Friend!) ✨",
        "description": "Your basil is thriving! This is the goal we were aiming for. 🌿",
        "symptoms": ["Vibrant green color", "No spots or discoloration", "Strong growth"],
        "care": ["Water regularly but don't overwater", "Provide 6-8 hours of sunlight daily", "Pinch off flower buds to promote leaf growth", "Harvest leaves frequently for bushier growth", "Keep room temperature 65-75°F"]
    },
    "Basil___unhealthy": {
        "name": "⚠️ Basil Needs Help! ⚠️",
        "description": "Your basil is showing signs of stress. Let's save it! This is exactly why I built this app—to help people like us save our plant friends. 💚",
        "symptoms": ["Yellowing leaves", "Brown spots or patches", "Wilting or drooping", "Stunted growth"],
        "care": [
            "🚨 IMMEDIATE: Check soil moisture—basil hates wet feet but needs consistent hydration",
            "💡 LIGHT: Move to a brighter location (6-8 hours of sunlight minimum)",
            "🌡️ TEMPERATURE: Basil loves warmth. Keep it between 65-75°F. Avoid cold drafts!",
            "✂️ PRUNE: Remove heavily damaged leaves to redirect energy",
            "🧪 HUMIDITY: Mist leaves lightly (basil likes moisture in the air, not on roots)",
            "🍽️ NUTRIENTS: Feed with balanced fertilizer every 2 weeks",
            "📦 REPOT: If soil looks compacted, repot into fresh, well-draining soil",
            "💪 PATIENCE: Recovery takes 1-2 weeks. You've got this!"
        ]
    },
    "Blueberry___healthy": {
        "name": "Healthy Blueberry",
        "description": "Your blueberry plant is doing well!",
        "symptoms": ["Normal green leaves", "No visible damage"],
        "care": ["Maintain acidic soil pH 4.5-5.5", "Regular watering during growing season", "Mulch to retain moisture", "Prune dead wood"]
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "name": "Cherry Powdery Mildew",
        "description": "Fungal disease creating a powdery white coating on leaves",
        "symptoms": ["White powdery coating on leaves", "Distorted leaf shape", "Reduced photosynthesis"],
        "care": ["Improve air circulation", "Remove heavily infected leaves", "Apply sulfur fungicide", "Water at base of plant"]
    },
    "Cherry_(including_sour)___healthy": {
        "name": "Healthy Cherry",
        "description": "Your cherry tree looks healthy!",
        "symptoms": ["Green, undamaged leaves"],
        "care": ["Water regularly", "Prune in winter", "Watch for pests", "Ensure good drainage"]
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "name": "Corn Cercospora Leaf Spot",
        "description": "Fungal disease causing gray-brown rectangular lesions",
        "symptoms": ["Gray-brown spots with purple halos", "Rectangular lesion shape", "Progressive yellowing"],
        "care": ["Remove infected leaves", "Improve drainage", "Rotate crops", "Apply fungicide if severe"]
    },
    "Corn_(maize)___Common_rust_": {
        "name": "Corn Common Rust",
        "description": "Fungal disease causing rust-colored pustules on leaves",
        "symptoms": ["Rusty red pustules on leaves", "Yellow halos around lesions", "Premature leaf death"],
        "care": ["Plant resistant varieties", "Improve air circulation", "Remove infected leaves", "Apply fungicide"]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "name": "Corn Northern Leaf Blight",
        "description": "Fungal disease causing cigar-shaped lesions on leaves",
        "symptoms": ["Tan or grayish lesions", "Cigar-shaped appearance", "Multiple lesions on single leaf"],
        "care": ["Rotate crops yearly", "Remove crop residue", "Plant resistant varieties", "Apply fungicide"]
    },
    "Corn_(maize)___healthy": {
        "name": "Healthy Corn",
        "description": "Your corn plant is in great condition!",
        "symptoms": ["Green, vigorous leaves", "No visible disease"],
        "care": ["Regular watering", "Ensure proper nutrition", "Monitor for pests", "Support tall varieties"]
    },
    "Grape___Black_rot": {
        "name": "Grape Black Rot",
        "description": "Fungal disease causing dark, sunken lesions on fruit and leaves",
        "symptoms": ["Dark brown lesions on fruit", "Black specks inside lesions", "Mummified fruit"],
        "care": ["Prune affected areas", "Remove mummified fruit", "Improve air circulation", "Apply fungicide"]
    },
    "Grape___Esca_(Black_Measles)": {
        "name": "Grape Esca (Black Measles)",
        "description": "Serious fungal disease affecting vascular system",
        "symptoms": ["Leaf mottling and striping", "Interveinal necrosis", "Sudden vine collapse"],
        "care": ["Prune out infected wood", "Sterilize tools between cuts", "Remove infected vines", "Consult specialist"]
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "name": "Grape Leaf Blight",
        "description": "Fungal disease causing small leaf spots and defoliation",
        "symptoms": ["Small circular spots", "Yellow halos", "Progressive leaf drop"],
        "care": ["Remove infected leaves", "Improve drainage", "Thin canopy", "Apply fungicide"]
    },
    "Grape___healthy": {
        "name": "Healthy Grape",
        "description": "Your grape vine is doing well!",
        "symptoms": ["Green, healthy leaves"],
        "care": ["Regular pruning", "Support structure maintenance", "Monitor for pests", "Proper irrigation"]
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "name": "Orange Huanglongbing (Citrus Greening)",
        "description": "Serious bacterial disease that is extremely damaging to citrus",
        "symptoms": ["Yellowing of veins first", "Blotchy yellowing", "Stunted fruit, bitter taste"],
        "care": ["No cure exists - tree removal recommended", "Control insect vectors (psyllids)", "Quarantine infected trees", "Plant resistant varieties"]
    },
    "Peach___Bacterial_spot": {
        "name": "Peach Bacterial Spot",
        "description": "Bacterial disease causing lesions on fruit and foliage",
        "symptoms": ["Small, dark, circular spots", "Yellow halos around spots", "Scabby fruit appearance"],
        "care": ["Apply copper fungicide", "Prune affected branches", "Avoid overhead watering", "Remove fallen fruit"]
    },
    "Peach___healthy": {
        "name": "Healthy Peach",
        "description": "Your peach tree looks great!",
        "symptoms": ["Healthy foliage"],
        "care": ["Regular pruning", "Thinning fruit", "Monitor for pests", "Proper watering"]
    },
    "Pepper,_bell___Bacterial_spot": {
        "name": "Bell Pepper Bacterial Spot",
        "description": "Bacterial disease causing water-soaked lesions",
        "symptoms": ["Small, dark, circular lesions", "Yellow halos", "Water-soaked appearance"],
        "care": ["Remove infected leaves", "Apply copper-based bactericide", "Improve air circulation", "Avoid wetting foliage"]
    },
    "Pepper,_bell___healthy": {
        "name": "Healthy Bell Pepper",
        "description": "Your pepper plant is thriving!",
        "symptoms": ["Green, healthy leaves"],
        "care": ["Consistent watering", "Full sunlight", "Support for heavy fruit", "Regular fertilizing"]
    },
    "Potato___Early_blight": {
        "name": "Potato Early Blight",
        "description": "Fungal disease causing dark lesions with concentric rings",
        "symptoms": ["Target-like lesions with concentric rings", "Starting on lower leaves", "Progressive upward spread"],
        "care": ["Remove lower leaves", "Improve air circulation", "Mulch soil", "Apply fungicide"]
    },
    "Potato___Late_blight": {
        "name": "Potato Late Blight",
        "description": "Serious fungal disease causing rapid crop destruction",
        "symptoms": ["Water-soaked lesions", "White fungal growth on leaf undersides", "Complete leaf collapse"],
        "care": ["Remove infected plants immediately", "Destroy plant material", "Improve drainage", "Apply protectant fungicide"]
    },
    "Potato___healthy": {
        "name": "Healthy Potato Plant",
        "description": "Your potato plant is healthy!",
        "symptoms": ["Green, vigorous foliage"],
        "care": ["Hill soil around stems", "Consistent watering", "Monitor for insects", "Proper spacing"]
    },
    "Raspberry___healthy": {
        "name": "Healthy Raspberry",
        "description": "Your raspberry cane is doing well!",
        "symptoms": ["Green, healthy leaves"],
        "care": ["Annual pruning", "Support structure", "Regular watering", "Weed management"]
    },
    "Soybean___healthy": {
        "name": "Healthy Soybean",
        "description": "Your soybean plant looks great!",
        "symptoms": ["Green foliage"],
        "care": ["Proper spacing", "Weed control", "Monitor for pests", "Adequate moisture"]
    },
    "Squash___Powdery_mildew": {
        "name": "Squash Powdery Mildew",
        "description": "Fungal disease covering leaves with white powder",
        "symptoms": ["White powdery coating", "Yellowing leaves", "Reduced fruit quality"],
        "care": ["Remove infected leaves", "Improve air circulation", "Apply sulfur spray", "Water at soil level"]
    },
    "Strawberry___Leaf_scorch": {
        "name": "Strawberry Leaf Scorch",
        "description": "Fungal disease causing leaf browning and necrosis",
        "symptoms": ["Brown, scorched leaf edges", "Tan centers in lesions", "Leaf curl"],
        "care": ["Remove infected leaves", "Improve drainage", "Space plants widely", "Apply fungicide"]
    },
    "Strawberry___healthy": {
        "name": "Healthy Strawberry",
        "description": "Your strawberry plant is thriving!",
        "symptoms": ["Green, healthy leaves"],
        "care": ["Remove runners if not propagating", "Mulch between plants", "Regular watering", "Fertilize monthly"]
    },
    "Tomato___Bacterial_spot": {
        "name": "Tomato Bacterial Spot",
        "description": "Bacterial disease causing small, dark, greasy lesions",
        "symptoms": ["Small, dark, circular spots", "Yellow halos", "Greasy appearance"],
        "care": ["Remove infected leaves", "Apply copper bactericide", "Avoid wetting foliage", "Remove lower leaves"]
    },
    "Tomato___Early_blight": {
        "name": "Tomato Early Blight",
        "description": "Fungal disease causing target-like lesions starting on lower leaves",
        "symptoms": ["Concentric ring pattern", "Starting on older leaves", "Progressive upward spread"],
        "care": ["Remove lower leaves proactively", "Improve air circulation", "Mulch soil", "Apply fungicide"]
    },
    "Tomato___Late_blight": {
        "name": "Tomato Late Blight",
        "description": "Serious fungal disease that destroyed tomato crops historically",
        "symptoms": ["Water-soaked lesions", "White fungal growth on undersides", "Rapid plant death"],
        "care": ["Remove infected plants immediately", "Improve air circulation", "Avoid overhead watering", "Apply protective fungicide"]
    },
    "Tomato___Leaf_Mold": {
        "name": "Tomato Leaf Mold",
        "description": "Fungal disease causing olive-green mold on leaf undersides",
        "symptoms": ["Olive-green fuzzy growth on undersides", "Yellow spots on upper surface", "Leaf yellowing"],
        "care": ["Increase air circulation", "Lower humidity", "Remove infected leaves", "Apply fungicide"]
    },
    "Tomato___Septoria_leaf_spot": {
        "name": "Tomato Septoria Leaf Spot",
        "description": "Fungal disease causing small, circular lesions with dark borders",
        "symptoms": ["Small circular spots with gray centers", "Dark borders", "Black specks in centers"],
        "care": ["Remove infected leaves", "Improve air circulation", "Mulch soil", "Apply fungicide"]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "name": "Tomato Spider Mites",
        "description": "Pest infestation causing fine webbing and leaf damage",
        "symptoms": ["Fine webbing on leaves", "Stippled, yellowing leaves", "Tiny moving specks"],
        "care": ["Increase humidity by misting", "Spray with water to remove webs", "Apply neem oil", "Release predatory mites"]
    },
    "Tomato___Target_Spot": {
        "name": "Tomato Target Spot",
        "description": "Fungal disease causing concentric ring lesions",
        "symptoms": ["Target-like lesions with concentric rings", "Brown center", "Yellow halo"],
        "care": ["Remove infected leaves", "Improve air circulation", "Mulch", "Apply fungicide"]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "name": "Tomato Yellow Leaf Curl Virus",
        "description": "Serious viral disease transmitted by whiteflies",
        "symptoms": ["Yellowing of leaf edges", "Leaf curling upward", "Stunted growth", "No fruit development"],
        "care": ["Remove infected plants", "Control whiteflies", "Use reflective mulch", "Plant resistant varieties"]
    },
    "Tomato___Tomato_mosaic_virus": {
        "name": "Tomato Mosaic Virus",
        "description": "Viral disease causing mottling and distortion",
        "symptoms": ["Mottled, variegated leaves", "Distorted leaf shape", "Stunted growth"],
        "care": ["Remove infected plants", "Disinfect tools", "Don't smoke near plants", "Plant resistant varieties"]
    },
    "Tomato___healthy": {
        "name": "Healthy Tomato Plant",
        "description": "Your tomato plant is looking great!",
        "symptoms": ["Green, healthy foliage"],
        "care": ["Consistent watering", "Proper staking/support", "Prune suckers", "Monitor for common diseases"]
    }
}

# ============================================
# MODEL LOADING (WITH CACHING)
# ============================================

@st.cache_resource
def load_model():
    """Load pre-trained Swin model"""
    model_path = "models/best_model.pth"
    processor_name = "microsoft/swin-base-patch4-window7-224"
    
    # Load processor
    processor = AutoImageProcessor.from_pretrained(processor_name)
    
    # Load model
    model = AutoModelForImageClassification.from_pretrained(
        processor_name,
        num_labels=40,``
        ignore_mismatched_sizes=True
    )
    
    # Load trained weights
    checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    return model, processor

@st.cache_resource
def load_label_mapping():
    """Load class label mapping"""
    with open("data/label_mapping.json", 'r') as f:
        mapping = json.load(f)
    return mapping['id2label']

# ============================================
# INFERENCE FUNCTION
# ============================================

def predict_disease(image, model, processor, id2label):
    """Predict disease from image"""
    # Preprocess image
    inputs = processor(images=image, return_tensors="pt")
    
    # Inference
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get probabilities
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    
    # Get top 5 predictions
    top_5_probs, top_5_indices = torch.topk(probabilities[0], k=5)
    
    predictions = []
    for prob, idx in zip(top_5_probs, top_5_indices):
        predictions.append({
            'label': id2label[str(int(idx))],
            'confidence': float(prob) * 100
        })
    
    return predictions

# ============================================
# MAIN APP
# ============================================

def main():
    # Load model and data
    model, processor = load_model()
    id2label = load_label_mapping()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌿 Plant Health Guardian</h1>
        <p><i>AI-powered plant disease detection to keep your green friends thriving</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("About This App")
    st.sidebar.info("""
    **Plant Health Guardian** uses AI (Swin Transformer) trained on 66,000+ plant images to:
    
    ✅ Identify diseases accurately (99.87% accuracy!)
    ✅ Provide care recommendations
    ✅ Suggest preventive measures
    ✅ Help save your beloved plants
    
    **Special feature:** This app was built with love for plant lovers everywhere—especially those of us who've struggled with raising basil! 💚
    """)
    
    # Sidebar - Developer story
    st.sidebar.markdown("---")
    st.sidebar.header("📖 The Story Behind This App")
    st.sidebar.write("""
    I once tried to grow basil in my dorm room. It started beautiful and vibrant, but slowly... the leaves yellowed, drooped, and eventually died. 😔
    
    I didn't know what went wrong. Was it too much water? Not enough light? Wrong temperature?
    
    That's why I built this app—to help people like me understand what's happening with our plants and save them before it's too late. Because every plant deserves a chance! 🌱
    """)
    
    # Main content
    col1, col2 = st.columns([1.5, 1.5])
    
    with col1:
        st.header("📸 Upload Plant Photo")
        uploaded_file = st.file_uploader(
            "Choose a leaf or plant photo (JPG, PNG)",
            type=['jpg', 'jpeg', 'png']
        )
    
    with col2:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Take a clear photo** of the affected leaf or plant
        2. **Ensure good lighting** for better accuracy
        3. **Focus on the leaf** - the model works best with leaf close-ups
        4. **Upload the image** and wait for the analysis
        """)
    
    # Process uploaded image
    if uploaded_file is not None:
        st.markdown("---")
        
        # Display image
        image = Image.open(uploaded_file)
        
        col_img, col_pred = st.columns([1, 1.5])
        
        with col_img:
            st.subheader("Your Photo")
            st.image(image, use_container_width=True)
        
        with col_pred:
            st.subheader("🤖 Analysis Running...")
            
            # Predict
            with st.spinner("Analyzing your plant... 🔍"):
                predictions = predict_disease(image, model, processor, id2label)
            
            # Get top prediction
            top_pred = predictions[0]
            top_label = top_pred['label']
            top_confidence = top_pred['confidence']
            
            # Display confidence bar
            st.markdown(f"### Top Match: **{top_label}**")
            
            confidence_pct = int(top_confidence)
            st.markdown(f"""
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: {confidence_pct}%">
                    {confidence_pct}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display top 5 predictions
            st.subheader("Top 5 Predictions")
            for i, pred in enumerate(predictions, 1):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"{i}. {pred['label']}")
                with cols[1]:
                    st.write(f"{pred['confidence']:.1f}%")
        
        # Disease details
        st.markdown("---")
        st.subheader("📋 Disease Details & Care Recommendations")
        
        disease_data = DISEASE_INFO.get(top_label, {})
        
        # Color card based on health status
        is_healthy = "healthy" in top_label.lower()
        card_class = "healthy-card" if is_healthy else "disease-card"
        
        st.markdown(f"""
        <div class="{card_class}">
            <h3>{disease_data.get('name', 'Unknown')}</h3>
            <p><i>{disease_data.get('description', '')}</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Symptoms
        st.subheader("🔍 Common Symptoms")
        for symptom in disease_data.get('symptoms', []):
            st.write(f"• {symptom}")
        
        # Care recommendations
        st.subheader("💚 Care & Treatment")
        for care in disease_data.get('care', []):
            st.markdown(f'<div class="care-tip">{care}</div>', unsafe_allow_html=True)
        
        # Special encouragement for basil
        if "Basil" in top_label:
            st.markdown("---")
            if "unhealthy" in top_label:
                st.info("""
                💪 **You can save your basil!** 
                
                Don't give up! Many plants recover with the right care. Follow the recommendations above, 
                be patient (recovery takes 1-2 weeks), and check on your plant daily. You've got this! 🌿
                """)
            else:
                st.success("""
                🎉 **Your basil is thriving!** 
                
                This is exactly what we want to see! Keep doing what you're doing. Enjoy harvesting fresh basil 
                for your cooking. The reward for good plant parenting! 🌱
                """)
        
        # Footer
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model Accuracy", "99.87%")
        with col2:
            st.metric("Plants Analyzed", "40 types")
        with col3:
            st.metric("Timestamp", datetime.now().strftime("%H:%M"))

if __name__ == "__main__":
    main()