import streamlit as st
import pytesseract
from PIL import Image, ImageEnhance, ImageOps

# 👉 Ако си на Windows:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="Food Scanner", page_icon="🍔")

st.title("🍔 Food Ingredients Scanner")
st.write("Качи снимка на съставките и ще проверим за вредни вещества.")

# ❌ Списък с вредни съставки
bad_ingredients = [
    "palm oil", "e621", "e250", "e951",
    "aspartame", "monosodium glutamate",
    "hydrogenated", "preservative",
    "colorant", "artificial flavor",
    "палмово масло", "глутамат", "консервант"
]

# 🧠 Функция за OCR preprocessing
def preprocess_image(image):
    gray = ImageOps.grayscale(image)  # grayscale
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(2.0)      # повече контраст
    return gray

# 🔍 Функция за анализ
def analyze_text(text):
    found = []
    for ingredient in bad_ingredients:
        if ingredient in text.lower():
            found.append(ingredient)
    return found

# 📂 Upload
uploaded_file = st.file_uploader("📷 Качи изображение", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_container_width=True)

    processed = preprocess_image(image)

    # 🧾 OCR
    text = pytesseract.image_to_string(processed, config="--psm 6")

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

    text = pytesseract.image_to_string(processed, config="--psm 6")

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
