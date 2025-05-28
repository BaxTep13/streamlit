import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Заголовок
st.title("🛍️ Poizon Style Generator")

# Загрузка изображения
uploaded_file = st.file_uploader("Загрузите фото товара", type=["jpg", "png", "jpeg"])
order_text = st.text_input("Текст заказа", "3akaa B PoizonShop")
model = st.text_input("Название модели", "PUMA Speedcat")
version = st.text_input("Версия", "OG")
size = st.text_input("Размер", "37.5")
price = st.text_input("Цена", "16 690 ₽")

if st.button("Создать карточку"):
    if uploaded_file:
        try:
            # Загрузка и подготовка изображения
            img = Image.open(uploaded_file).convert("RGBA")
            img = ImageOps.exif_transpose(img)
            
            text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(text_layer)

            # Градиентная подложка
            gradient = Image.new("L", (img.width, img.height), 0)
            for y in range(img.height):
                if y >= img.height - 220:
                    alpha = int(180 * ((y - (img.height - 220)) / 220))
                    for x in range(img.width):
                        gradient.putpixel((x, y), alpha)
            text_layer.putalpha(gradient)

            # Шрифты
            try:
                font_small = ImageFont.truetype("arial.ttf", 24)
                font_large = ImageFont.truetype("arialbd.ttf", 54)
                font_medium = ImageFont.truetype("arialbd.ttf", 42)
                font_price = ImageFont.truetype("arialbd.ttf", 60)
            except:
                font_small = ImageFont.load_default()
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_price = ImageFont.load_default()

            # Наложение текста
            draw.text((40, img.height - 200), order_text, font=font_small, fill="#AAAAAA")
            draw.text((40, img.height - 170), model, font=font_large, fill="white")
            draw.text((40, img.height - 110), version, font=font_medium, fill="white")
            
            size_text = f"Размер: {size}"
            size_width = draw.textlength(size_text, font=font_large)
            draw.text((img.width - size_width - 40, img.height - 170), size_text, font=font_large, fill="white")

            price_bg_width = draw.textlength(price, font=font_price) + 40
            price_bg = Image.new("RGBA", (int(price_bg_width), 80), (255, 59, 48, 240))
            text_layer.paste(price_bg, (img.width - int(price_bg_width), img.height - 100), price_bg)
            draw.text((img.width - int(price_bg_width) + 20, img.height - 100), price, font=font_price, fill="white")

            result = Image.alpha_composite(img, text_layer).convert("RGB")

            st.image(result, caption="Ваша карточка в стиле Poizon", use_column_width=True)

            # Скачивание
            st.download_button(
                label="📥 Скачать изображение",
                data=result_to_bytes(result),
                file_name="poizon_card.jpg",
                mime="image/jpeg"
            )

        except Exception as e:
            st.error(f"❌ Ошибка: {str(e)}")
    else:
        st.warning("Пожалуйста, загрузите изображение!")

def result_to_bytes(image):
    from io import BytesIO
    buf = BytesIO()
    image.save(buf, format="JPEG")
    buf.seek(0)
    return buf
