import streamlit as st
import easyocr
import pandas as pd
from PIL import Image
import tempfile
import os
import numpy as np

# OCR okuyucu
reader = easyocr.Reader(['en'])

def ocr_image(image_path):
    image = Image.open(image_path)
    image_np = np.array(image)
    result = reader.readtext(image_np, detail=0)
    text = " ".join(result)
    return text

def find_harmful_ingredients(text, dataset):
    harmful_found = []
    text_lower = text.lower()

    for _, row in dataset.iterrows():
        madde = str(row["additive"]).lower()  
        aciklama = row["description"]        

        if madde in text_lower:
            harmful_found.append((madde, aciklama))

    return harmful_found

st.title("📸 Gıda Katkı Maddesi Tanıma Uygulaması")
st.write("Kameranı kullanarak **içindekiler** kısmını çek, biz zararlı maddeleri açıklayalım.")

camera_image = st.camera_input("📷 Kamerayla fotoğraf çek")

if camera_image:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(camera_image.getvalue())
        temp_path = tmp_file.name

    image = Image.open(temp_path)
    st.image(image, caption="Çekilen Görsel", use_container_width=True)
    st.write("Görseli analiz ediyoruz...")


    with st.spinner("Metin analiz ediliyor..."):
        try:
            text = ocr_image(temp_path)
            dataset = pd.read_csv("additives.csv")  
            harmful_items = find_harmful_ingredients(text, dataset)
        except Exception as e:
            st.error(f"Hata oluştu: {str(e)}")
            harmful_items = []

    st.subheader("📄 Tespit Edilen Metin:")
    st.write(text)

    st.subheader("⚠️ Zararlı Maddeler:")
    if harmful_items:
        for madde, aciklama in harmful_items:
            st.markdown(f"- **{madde.upper()}**: {aciklama}")
    else:
        st.success("Zararlı katkı maddesi bulunamadı. ✅")

    os.remove(temp_path)
