import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# ページの設定
st.set_page_config(page_title="バスケ作戦盤", layout="centered")

st.title("🏀 バスケ作戦盤")
st.write("ツールを選んでコートに描き込んでください。「Transform」で描いたものを動かせます。")

# --- サイドボード（設定エリア） ---
st.sidebar.header("ツール設定")

# 描画モードの選択
drawing_mode = st.sidebar.selectbox(
    "描画モード:", ("freedraw", "line", "circle", "transform")
)

# ペンの太さと色の設定
stroke_width = st.sidebar.slider("線の太さ:", 1, 20, 3)
stroke_color = st.sidebar.color_picker("ペンの色:", "#FF0000")
bg_color = "#084d0d" # コートの背景色（画像がない場合の予備）

# --- コート画像の準備 ---
# 本来はリポジトリにcourt.pngを置くのがベストですが、
# 今回は簡易的に背景色のみ、またはネット上のフリー画像URLを指定する形にします。
# ※ 自分のコート画像を使いたい場合は、画像ファイルをGitHubに上げ、
# Image.open("court.png") と書き換えてください。
bg_image_url = "https://raw.githubusercontent.com/andfanilo/streamlit-drawable-canvas-demo/master/img/basketball_court.png"

# --- キャンバスの実装 ---
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # 図形の中身の色
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=Image.open(st.cache_data(lambda: Image.open(import_requests().get(bg_image_url, stream=True).raw))()) if False else None, # 画像読み込みは環境に依存するため一旦シンプルに
    update_streamlit=True,
    height=600,
    width=500,
    drawing_mode=drawing_mode,
    key="canvas",
)

# 補足：ネット上の画像を表示させるための工夫（もし画像URLを使う場合）
# 実際にはリポジトリに画像を同梱するのが一番確実です！

st.info("【操作ヒント】\n- circle: 選手を配置\n- freedraw: 動きを描く\n- line: パスを描く\n- transform: 配置した選手や線を指で動かす")