import streamlit as st
import easyocr
from PIL import Image, ImageEnhance, ImageOps
import numpy as np

st.set_page_config(page_title="Food Scanner", page_icon="🍔")

st.title("🍔 Food Ingredients Scanner (EasyOCR)")
st.write("Качи снимка на съставките и ще проверим за вредни вещества.")

# ❌ Списък с вредни съставки
bad_ingredients = [
    "palm oil", "e621", "e250", "e951",
    "aspartame", "monosodium glutamate",
    "hydrogenated", "preservative",
    "colorant", "artificial flavor",
    "палмово масло", "глутамат", "консервант"
]

# 🧠 OCR reader (зарежда се веднъж)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en', 'bg'], gpu=False)

reader = load_reader()

# 🧠 preprocessing
def preprocess_image(image):
    gray = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(2.0)
    return gray

# 🔍 анализ
def analyze_text(text):
    found = []
    for ingredient in bad_ingredients:
        if ingredient in text.lower():
            found.append(ingredient)
    return found

# 🔤 OCR функция
def run_ocr(image):
    img = np.array(image)
    results = reader.readtext(img)
    
    texts = [res[1] for res in results]
    full_text = " ".join(texts)
    
    return full_text

# 📂 Upload
uploaded_file = st.file_uploader("📷 Качи изображение", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_container_width=True)

    processed = preprocess_image(image)

    # 🧾 OCR
    text = run_ocr(processed)

    st.subheader("📄 Разпознат текст:")
    st.text(text)

    st.subheader("🔍 Анализ на съставките:")

    found_items = analyze_text(text)

    if found_items:
        st.error("❌ Открити вредни съставки:")
        for item in found_items:
            st.write(f"- {item}")
    else:
        st.success("✅ Не са открити вредни съставки")

# 📷 Камера
st.divider()
st.subheader("📷 Или снимай директно")

camera_image = st.camera_input("Направи снимка")

if camera_image:
    image = Image.open(camera_image)
    st.image(image, caption="Снимка от камера", use_container_width=True)

    processed = preprocess_image(image)

    text = run_ocr(processed)

    st.subheader("📄 Разпознат текст:")
    st.text(text)

    st.subheader("🔍 Анализ:")

    found_items = analyze_text(text)

    if found_items:
        st.error("❌ Открити вредни съставки:")
        for item in found_items:
            st.write(f"- {item}")
    else:
        st.success("✅ Не са открити вредни съставки")
