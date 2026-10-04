import streamlit as st
import numpy as np
import cv2
from PIL import Image
from pathlib import Path
import tensorflow as tf
import json

from nutrition_map import get_nutrition

# =========================
# Setup
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = OUT_DIR / "model_food.keras"
CLASSES_PATH = OUT_DIR / "class_names.txt"

st.set_page_config(page_title="Food Recognition + Info Gizi", layout="wide")

# =========================
# Helpers
# =========================
def pil_to_bgr(pil_img: Image.Image) -> np.ndarray:
    rgb = np.array(pil_img.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

def bgr_to_pil(bgr: np.ndarray) -> Image.Image:
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)

def auto_crop_food(bgr: np.ndarray) -> np.ndarray:
    """Auto crop sederhana pakai kontur terbesar."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # kalau kebanyakan putih, invert
    if (th == 255).mean() > 0.75:
        th = cv2.bitwise_not(th)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return bgr

    c = max(cnts, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    pad = int(0.06 * max(w, h))
    x2 = max(0, x - pad)
    y2 = max(0, y - pad)
    x3 = min(bgr.shape[1], x + w + pad)
    y3 = min(bgr.shape[0], y + h + pad)

    return bgr[y2:y3, x2:x3]

@st.cache_resource
def load_model_and_classes():
    if not MODEL_PATH.exists() or not CLASSES_PATH.exists():
        return None, None
    model = tf.keras.models.load_model(MODEL_PATH)
    class_names = CLASSES_PATH.read_text(encoding="utf-8").splitlines()
    return model, class_names

def predict_label_from_crop(crop_bgr: np.ndarray):
    model, class_names = load_model_and_classes()
    if model is None:
        return None, 0.0

    crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
    crop_res = cv2.resize(crop_rgb, (224, 224), interpolation=cv2.INTER_AREA)
    x = crop_res.astype("float32")
    x = np.expand_dims(x, axis=0)

    probs = model.predict(x, verbose=0)[0]
    idx = int(np.argmax(probs))
    conf = float(probs[idx])
    label = class_names[idx]
    return label, conf

# =========================
# UI
# =========================
st.title("🍽️ Food Recognition (51 Kelas) + Info Gizi")
st.caption("Upload gambar → Auto crop → Prediksi model → Info gizi tampil di kanan.")

uploaded = st.file_uploader("Upload gambar makanan (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded is None:
    st.info("Upload gambar dulu ya.")
    st.stop()

bgr = pil_to_bgr(Image.open(uploaded))

st.sidebar.header("Pengaturan")
crop_mode = st.sidebar.selectbox("Crop Mode", ["Auto", "Manual"])
save_outputs = st.sidebar.checkbox("Simpan hasil ke outputs/", value=True)

# Manual crop
if crop_mode == "Manual":
    H, W = bgr.shape[:2]
    x = st.sidebar.slider("x", 0, W - 1, 0)
    y = st.sidebar.slider("y", 0, H - 1, 0)
    cw = st.sidebar.slider("width", 1, W - x, min(400, W - x))
    ch = st.sidebar.slider("height", 1, H - y, min(400, H - y))
    crop_bgr = bgr[y:y+ch, x:x+cw]
else:
    crop_bgr = auto_crop_food(bgr)

# Prediksi
pred_label, conf = predict_label_from_crop(crop_bgr)
if pred_label is None:
    st.error("Model tidak ditemukan. Pastikan outputs/model_food.keras dan outputs/class_names.txt ada.")
    st.stop()

nutri = get_nutrition(pred_label)

# Layout
col1, col2 = st.columns([1.35, 1.0], gap="large")

with col1:
    st.subheader("Gambar Asli")
    st.image(bgr_to_pil(bgr), use_container_width=True)

    st.subheader("Crop")
    st.image(bgr_to_pil(crop_bgr), use_container_width=True)

with col2:
    st.subheader("Prediksi + Info Gizi")
    st.write(f"**Label:** {nutri['display_name']}")
    st.write(f"**Confidence:** {conf:.3f}")
    st.write(f"**Status gizi:** `{nutri['status']}`")

    n = nutri["nutrition"]
    st.markdown("### Nutrisi")
    st.write(f"**Basis:** {n.get('basis')}")
    st.write(f"**Kalori:** {n.get('calories')} kcal")
    st.write(f"**Protein:** {n.get('protein')} g")
    st.write(f"**Lemak:** {n.get('fat')} g")
    st.write(f"**Karbohidrat:** {n.get('carbohydrate')} g")
    st.caption(f"match_source: {nutri.get('match_source')}")

    result = {
        "filename": uploaded.name,
        "predicted_label": pred_label,
        "confidence": float(conf),
        "display_name": nutri["display_name"],
        "nutrition": nutri["nutrition"],
        "nutrition_status": nutri["status"],
        "nutrition_match_source": nutri["match_source"],
        "crop_mode": crop_mode,
    }

    if save_outputs and st.button("💾 Simpan hasil"):
        out_json = OUT_DIR / "predict_result.json"
        out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

        out_crop = OUT_DIR / "crop.png"
        cv2.imwrite(str(out_crop), crop_bgr)

        st.success("✅ Disimpan ke outputs/")
        st.write(f"- `{out_json}`")
        st.write(f"- `{out_crop}`")
