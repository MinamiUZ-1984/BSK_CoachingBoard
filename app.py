import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(page_title="バスケ作戦盤", layout="centered")
st.title("🏀 バスケ作戦盤（安定版）")

# 1. セッション（記憶）の初期化
if "shapes" not in st.session_state:
    st.session_state.shapes = []

# 2. コート画像を生成する関数
def get_court_base():
    # 強制的にオレンジ色の画像を作る
    width, height = 350, 520
    img = Image.new("RGB", (width, height), "#FF8C00") 
    draw = ImageDraw.Draw(img)
    
    # 白いラインを描く
    line_color = "white"
    draw.rectangle([10, 10, 340, 510], outline=line_color, width=3) # 外枠
    draw.line([10, 260, 340, 260], fill=line_color, width=3) # センターライン
    draw.ellipse([135, 220, 215, 300], outline=line_color, width=3) # センターサークル
    return img

# 3. 操作パネル
col1, col2 = st.columns(2)
with col1:
    if st.button("最後の一手を消す"):
        if st.session_state.shapes:
            st.session_state.shapes.pop()
            st.rerun()
with col2:
    if st.button("全部消す（リセット）"):
        st.session_state.shapes = []
        st.rerun()

# 4. 描画処理
court = get_court_base()
draw = ImageDraw.Draw(court)

# 記憶している図形を描画
for shape in st.session_state.shapes:
    x, y, color = shape
    # タップした場所に丸を描く
    draw.ellipse([x-10, y-10, x+10, y+10], fill=color, outline="white")

# 5. 画像を表示し、クリック（タップ）を検知する
# label_visibility="collapsed" で余計な文字を消す
value = st.image_canvas = st.button("コートをタップして選手を配置", use_container_width=True)

# 重要：Streamlit標準のクリック検知（一部環境で対応）
# もしタップが難しい場合は、以下の標準画像表示に切り替えます
st.image(court, caption="コートをタップしてください（開発中）", use_container_width=True)

st.info("※現在、表示エンジンの切り替えテスト中です。オレンジ色のコートは見えていますか？")
