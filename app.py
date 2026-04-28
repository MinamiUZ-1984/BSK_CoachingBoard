import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw

# ページ設定
st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")

st.title("🏀 バスケ作戦盤 Pro")

# --- 1. コート画像の生成（オレンジ一色） ---
def create_court_image():
    # スマホ画面に合わせたサイズ
    width, height = 350, 520
    # 指定されたきれいなオレンジ色（#FF8C00）で画像を作成
    img = Image.new("RGB", (width, height), "#FF8C00") 
    # 描画オブジェクト (ImageDraw) は作成しない（何も描かないため）
    
    # ラインなどは描画せず、そのままオレンジ色の画像を返す
    return img

# --- 2. 選手とボールの初期位置データ ---
# これにより、起動時に最初からモノが配置されます
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
        # ボール (背景のオレンジと同化しないように黒のフチドリをつけています)
        {"type": "circle", "left": 175, "top": 260, "radius": 8,  "fill": "orange", "stroke": "black", "strokeWidth": 2}
    ]
}

# --- 3. UI操作エリア ---
st.write("### 🕹️ 操作パネル")
col1, col2, col3 = st.columns(3)
with col1:
    mode = st.radio("モード切替", ("動かす", "書く"), horizontal=True)
with col2:
    color = st.color_picker("ペンの色", "#FFFFFF") # 初期色は白
with col3:
    if st.button("リセット"):
        st.rerun()

# モードの変換
drawing_mode = "transform" if mode == "動かす" else "freedraw"

# --- 4. キャンバス実行 ---
# 背景画像として、さきほど生成した「オレンジ一色」のコート画像をセット
bg_image = create_court_image()

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # circleで描いた時の塗りつぶし色
    stroke_width=3,
    stroke_color=color,
    background_image=bg_image,          # ここでオレンジ画像を適用！
    initial_drawing=initial_objects,    # 選手とボールの初期配置
    update_streamlit=True,
    height=520,
    width=350,
    drawing_mode=drawing_mode,
    # キーを新しくしてキャッシュをリセット
    key="canvas_one_color_orange",
)

st.caption("※「動かす」モードで選手やボールをドラッグ、「書く」モードで線を引けます。")
