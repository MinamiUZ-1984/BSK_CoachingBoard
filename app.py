import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw

# ページ設定
st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")

st.title("🏀 バスケ作戦盤 Pro")

# --- 1. コート画像の生成（座標エラー修正済み） ---
def create_court_image():
    width, height = 350, 520
    img = Image.new("RGB", (width, height), "#dfbb85")
    draw = ImageDraw.Draw(img)
    line_color = "white"
    w = 3
    
    # 外枠
    draw.rectangle([10, 10, width-10, height-10], outline=line_color, width=w)
    
    # センターライン・サークル
    draw.line([10, height/2, width-10, height/2], fill=line_color, width=w)
    draw.ellipse([width/2 - 40, height/2 - 40, width/2 + 40, height/2 + 40], outline=line_color, width=w)
    
    # 上半分のコート
    draw.rectangle([width/2 - 45, 10, width/2 + 45, 120], outline=line_color, width=w)
    draw.line([width/2 - 25, 25, width/2 + 25, 25], fill="black", width=4) # バックボード
    
    # 下半分のコート（ここがエラーの原因でした。y座標の大小を修正）
    draw.rectangle([width/2 - 45, height-120, width/2 + 45, height-10], outline=line_color, width=w)
    draw.line([width/2 - 25, height-25, width/2 + 25, height-25], fill="black", width=4) # バックボード

    return img

# --- 2. 選手とボールの初期位置データ ---
initial_objects = {
    "version": "4.4.0",
    "objects": [
        # 赤チーム (5人)
        {"type": "circle", "left": 50,  "top": 150, "radius": 12, "fill": "red", "label": "R1"},
        {"type": "circle", "left": 120, "top": 150, "radius": 12, "fill": "red", "label": "R2"},
        {"type": "circle", "left": 190, "top": 150, "radius": 12, "fill": "red", "label": "R3"},
        {"type": "circle", "left": 260, "top": 150, "radius": 12, "fill": "red", "label": "R4"},
        {"type": "circle", "left": 310, "top": 150, "radius": 12, "fill": "red", "label": "R5"},
        # 青チーム (5人)
        {"type": "circle", "left": 50,  "top": 370, "radius": 12, "fill": "blue", "label": "B1"},
        {"type": "circle", "left": 120, "top": 370, "radius": 12, "fill": "blue", "label": "B2"},
        {"type": "circle", "left": 190, "top": 370, "radius": 12, "fill": "blue", "label": "B3"},
        {"type": "circle", "left": 260, "top": 370, "radius": 12, "fill": "blue", "label": "B4"},
        {"type": "circle", "left": 310, "top": 370, "radius": 12, "fill": "blue", "label": "B5"},
        # ボール
        {"type": "circle", "left": 175, "top": 260, "radius": 8,  "fill": "orange", "stroke": "black", "strokeWidth": 2}
    ]
}

# --- 3. UI操作エリア ---
st.write("### 🕹️ 操作パネル")
col1, col2, col3 = st.columns(3)
with col1:
    mode = st.radio("モード切替", ("動かす", "書く"), horizontal=True)
with col2:
    color = st.color_picker("ペンの色", "#000000")
with col3:
    if st.button("リセット"):
        st.rerun()

# モードの変換
drawing_mode = "transform" if mode == "動かす" else "freedraw"

# --- 4. キャンバス実行 ---
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=3,
    stroke_color=color,
    background_image=create_court_image(),
    initial_drawing=initial_objects,
    update_streamlit=True,
    height=520,
    width=350,
    drawing_mode=drawing_mode,
    key="canvas_pro",
)

st.caption("※「動かす」モードで選手をドラッグ、「書く」モードで線を引けます。")
