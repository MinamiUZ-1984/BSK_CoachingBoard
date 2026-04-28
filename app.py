import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw

# ページの設定
st.set_page_config(page_title="バスケ作戦盤", layout="centered")

st.title("🏀 バスケ作戦盤")

# --- コート画像を自動生成（スマホ向けに少し小さく調整） ---
def create_court_image():
    width, height = 350, 520  # iPhone等でも横スクロールが出ないサイズ
    img = Image.new("RGB", (width, height), "#dfbb85")
    draw = ImageDraw.Draw(img)
    
    line_color = "white"
    w = 3 
    
    # 外枠
    draw.rectangle([10, 10, width-10, height-10], outline=line_color, width=w)
    
    # ハーフウェイラインとセンターサークル
    draw.line([10, height/2, width-10, height/2], fill=line_color, width=w)
    draw.ellipse([width/2 - 40, height/2 - 40, width/2 + 40, height/2 + 40], outline=line_color, width=w)
    
    # 上半分のコート
    draw.rectangle([width/2 - 45, 10, width/2 + 45, 120], outline=line_color, width=w)
    draw.arc([width/2 - 45, 80, width/2 + 45, 160], 0, 180, fill=line_color, width=w) 
    draw.arc([30, -40, width-30, 210], 0, 180, fill=line_color, width=w) 
    draw.line([width/2 - 25, 25, width/2 + 25, 25], fill="black", width=4) 
    draw.ellipse([width/2 - 12, 25, width/2 + 12, 49], outline="red", width=3) 
    
    # 下半分のコート
    draw.rectangle([width/2 - 45, height-120, width/2 + 45, height-10], outline=line_color, width=w)
    draw.arc([width/2 - 45, height-160, width/2 + 45, height-80], 180, 360, fill=line_color, width=w) 
    draw.arc([30, height-210, width-30, height+40], 180, 360, fill=line_color, width=w) 
    draw.line([width/2 - 25, height-25, width/2 + 25, height-25], fill="black", width=4) 
    draw.ellipse([width/2 - 12, height-49, width/2 + 12, height-25], outline="red", width=3) 

    return img

# --- スマホでタップしやすいように、メニューをメイン画面に配置 ---
st.write("ツールを選んでコートをタップ・スワイプしてください。")

col1, col2 = st.columns(2)
with col1:
    drawing_mode = st.selectbox("ツール選択:", ("freedraw", "line", "circle", "transform"))
with col2:
    stroke_color = st.color_picker("ペンの色:", "#FF0000")

# --- キャンバスの実装 ---
bg_image = create_court_image()

canvas_result = st_canvas(
    fill_color="rgba(255, 0, 0, 0.7)", 
    stroke_width=3,
    stroke_color=stroke_color,
    background_image=bg_image,
    update_streamlit=True,
    height=520,
    width=350,
    drawing_mode=drawing_mode,
    key="canvas",
)
