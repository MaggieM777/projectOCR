import streamlit as st
import pytesseract
from PIL import Image
import numpy as np
import cv2

# 👉 Ако си на Windows, разкоментирай и сложи правилния път:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="Food Scanner", page_icon="🍔")

st.title("🍔 Food Ingredients Scanner")
st.write("Качи снимка на съставките и ще проверим за вредни вещества.")

# 📂 Upload
uploaded_file = st.file_uploader("📷 Качи изображение", type=["jpg", "jpeg", "png"])

# ❌ Списък с вредни съставки
bad_ingredients = [
    "palm oil", "e621", "e250", "e951",
    "aspartame", "monosodium glutamate",
    "hydrogenated", "preservative",
    "colorant", "artificial flavor",
    "палмово масло", "глутамат", "консервант"
]

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_container_width=True)

    # 🧠 Preprocessing (подобрява OCR)
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    # 🧾 OCR
    text = pytesseract.image_to_string(gray)

    st.subheader("📄 Разпознат текст:")
    st.text(text)

    # 🔍 Анализ
    st.subheader("🔍 Анализ на съставките:")

    found_items = []

    for ingredient in bad_ingredients:
        if ingredient in text.lower():
            found_items.append(ingredient)

    if found_items:
        st.error("❌ Открити вредни съставки:")
        for item in found_items:
            st.write(f"- {item}")
    else:
        st.success("✅ Не са открити вредни съставки")

# 📷 Камера (бонус)
st.divider()
st.subheader("📷 Или снимай директно")

camera_image = st.camera_input("Направи снимка")

if camera_image:
    image = Image.open(camera_image)
    st.image(image, caption="Снимка от камера", use_container_width=True)

    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    text = pytesseract.image_to_string(gray)

    st.subheader("📄 Разпознат текст:")
    st.text(text)

    st.subheader("🔍 Анализ:")

    found_items = []

    for ingredient in bad_ingredients:
        if ingredient in text.lower():
            found_items.append(ingredient)

    if found_items:
        st.error("❌ Открити вредни съставки:")
        for item in found_items:
            st.write(f"- {item}")
    else:
        st.success("✅ Не са открити вредни съставки")
