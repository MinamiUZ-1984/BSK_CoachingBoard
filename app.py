import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw

# ページの設定（スマホで見やすいように調整）
st.set_page_config(page_title="バスケ作戦盤", layout="centered")

st.title("🏀 バスケ作戦盤")

# --- コート画像を自動生成する関数 ---
def create_court_image():
    # スマホ画面に合わせた縦長のキャンバスサイズ
    width, height = 400, 600
    # 木目調のフロア色で塗りつぶし
    img = Image.new("RGB", (width, height), "#dfbb85")
    draw = ImageDraw.Draw(img)
    
    line_color = "white"
    w = 3 # 線の太さ
    
    # 1. コートの外枠 (余白10px)
    draw.rectangle([10, 10, width-10, height-10], outline=line_color, width=w)
    
    # 2. ハーフウェイラインとセンターサークル
    draw.line([10, height/2, width-10, height/2], fill=line_color, width=w)
    draw.ellipse([width/2 - 40, height/2 - 40, width/2 + 40, height/2 + 40], outline=line_color, width=w)
    
    # 3. 上半分のコート（ペイントエリア、3Pライン、ゴール）
    draw.rectangle([width/2 - 50, 10, width/2 + 50, 130], outline=line_color, width=w)
    draw.arc([width/2 - 50, 80, width/2 + 50, 180], 0, 180, fill=line_color, width=w) # フリースロー
    draw.arc([30, -50, width-30, 230], 0, 180, fill=line_color, width=w) # 3Pライン
    draw.line([width/2 - 25, 25, width/2 + 25, 25], fill="black", width=4) # バックボード
    draw.ellipse([width/2 - 12, 25, width/2 + 12, 49], outline="red", width=3) # リング
    
    # 4. 下半分のコート
    draw.rectangle([width/2 - 50, height-130, width/2 + 50, height-10], outline=line_color, width=w)
    draw.arc([width/2 - 50, height-180, width/2 + 50, height-80], 180, 360, fill=line_color, width=w) # フリースロー
    draw.arc([30, height-230, width-30, height+50], 180, 360, fill=line_color, width=w) # 3Pライン
    draw.line([width/2 - 25, height-25, width/2 + 25, height-25], fill="black", width=4) # バックボード
    draw.ellipse([width/2 - 12, height-49, width/2 + 12, height-25], outline="red", width=3) # リング

    return img

# --- サイドボード（設定エリア） ---
st.sidebar.header("ツール設定")
drawing_mode = st.sidebar.selectbox("描画モード:", ("freedraw", "line", "circle", "transform"))
stroke_width = st.sidebar.slider("線の太さ:", 1, 10, 3)
stroke_color = st.sidebar.color_picker("ペンの色:", "#FF0000")

st.info("【操作ヒント】\n- circle: 選手を配置\n- freedraw: 動きを描く\n- line: パスを描く\n- transform: 配置した選手や線を指で動かす")

# --- キャンバスの実装 ---
# 背景画像として、さきほど生成したコート画像をセット
bg_image = create_court_image()

canvas_result = st_canvas(
    fill_color="rgba(255, 0, 0, 0.7)",  # circleで描いた時の塗りつぶし色
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_image=bg_image,          # ここでコート画像を適用！
    update_streamlit=True,
    height=600,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)
