import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw

# ページ設定
st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")

# 更新されたことが一目でわかるようにタイトルを変更
st.title("🏀 バスケ作戦盤（グリーンver.）")

# --- 1. コート画像の生成（グリーン背景・白線） ---
def create_court_image():
    width, height = 350, 520
    # 背景を濃い緑色 (#228B22: ForestGreen) に設定
    img = Image.new("RGB", (width, height), "#228B22") 
    draw = ImageDraw.Draw(img)
    line_color = "white"
    w = 3
    
    # センターラインとサークルだけシンプルに描画（検証のため）
    draw.rectangle([10, 10, width-10, height-10], outline=line_color, width=w)
    draw.line([10, height/2, width-10, height/2], fill=line_color, width=w)
    draw.ellipse([width/2-40, height/2-40, width/2+40, height/2+40], outline=line_color, width=w)
    return img

# --- 2. 選手とボールの初期位置 ---
initial_objects = {
    "version": "4.4.0",
    "objects": [
        {"type": "circle", "left": 175, "top": 100, "radius": 15, "fill": "red", "label": "R"},
        {"type": "circle", "left": 175, "top": 420, "radius": 15, "fill": "blue", "label": "B"},
        {"type": "circle", "left": 175, "top": 260, "radius": 10, "fill": "orange", "stroke": "black", "strokeWidth": 2}
    ]
}

# --- 3. UI操作エリア ---
st.write("これが緑色に見えていれば、更新は成功しています！")
mode = st.radio("モード:", ("動かす", "書く"), horizontal=True)
drawing_mode = "transform" if mode == "動かす" else "freedraw"

# --- 4. キャンバス実行 ---
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.3)",
    stroke_width=3,
    stroke_color="white",
    background_color="#228B22", # ここでもグリーンを強制指定
    background_image=create_court_image(),
    initial_drawing=initial_objects,
    update_streamlit=True,
    height=520,
    width=350,
    drawing_mode=drawing_mode,
    key="canvas_green_test", # キーを新しくして記憶をリセット
)
