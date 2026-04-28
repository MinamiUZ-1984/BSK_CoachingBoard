import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

st.title("🏀 バスケ作戦盤（新起動）")

# シンプルな緑の背景画像
width, height = 350, 500
bg_img = Image.new("RGB", (width, height), "#228B22") # 緑色

# キャンバス設置
st_canvas(
    background_image=bg_img,
    height=height,
    width=width,
    drawing_mode="freedraw",
    key="new_board"
)
st.write("緑色の画面が見えていれば成功です！")
