import streamlit as st

st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")
st.title("🏀 バスケ作戦盤 Pro")

# --- 1. 選手とボールの位置記憶 ---
if "positions" not in st.session_state:
    st.session_state.positions = {
        "R1": [175, 150], "R2": [50, 200], "R3": [300, 200], "R4": [100, 260], "R5": [250, 260],
        "B1": [175, 370], "B2": [50, 320], "B3": [300, 320], "B4": [100, 260], "B5": [250, 260],
        "Ball": [175, 260]
    }

# --- 2. 操作パネル ---
st.write("### 🕹️ 配置設定")
target = st.selectbox("動かす対象:", list(st.session_state.positions.keys()))
col1, col2 = st.columns(2)
with col1:
    st.session_state.positions[target][0] = st.slider("左右 (X)", 0, 350, st.session_state.positions[target][0])
with col2:
    st.session_state.positions[target][1] = st.slider("前後 (Y)", 0, 520, st.session_state.positions[target][1])

# --- 3. コートを描画するSVG関数 (レイアウト修正版) ---
def draw_perfect_court():
    pos = st.session_state.positions
    c_orange = "#FF8C00"
    c_white = "white"
    
    svg = f'<svg width="350" height="520" viewBox="0 0 350 520" xmlns="http://www.w3.org/2000/svg">'
    svg += f'<rect width="350" height="520" fill="{c_orange}" />'
    style = f'fill="none" stroke="{c_white}" stroke-width="3"'
    
    # 基本ライン
    svg += f'<rect x="10" y="10" width="330" height="500" {style} />'
    svg += f'<line x1="10" y1="260" x2="340" y2="260" {style} />'
    svg += f'<circle cx="175" cy="260" r="40" {style} />'

    # --- 上半分のライン ---
    # ペイントエリア: ゴール側に寄せて少し短く (10〜120までに短縮)
    svg += f'<rect x="135" y="10" width="80" height="110" {style} />'
    # フリースローサークル: 位置を120に移動
    svg += f'<circle cx="175" cy="120" r="40" {style} />'
    # 3Pライン: 下方向(センターライン側)へシフトし、サークルと離す
    svg += f'<path d="M 30 10 A 150 150 0 0 0 320 10" {style} transform="translate(0, 45)" />'
    # ゴール
    svg += f'<line x1="150" y1="35" x2="200" y2="35" stroke="black" stroke-width="4" />'
    svg += f'<circle cx="175" cy="50" r="12" stroke="red" stroke-width="3" fill="none" />'

    # --- 下半分のライン ---
    # ペイントエリア: ゴール側に寄せて短く (410〜510)
    svg += f'<rect x="135" y="410" width="80" height="100" {style} />'
    # フリースローサークル: 位置を400に移動
    svg += f'<circle cx="175" cy="400" r="40" {style} />'
    # 3Pライン: 上方向(センターライン側)へシフト
    svg += f'<path d="M 30 510 A 150 150 0 0 1 320 510" {style} transform="translate(0, -45)" />'
    # ゴール
    svg += f'<line x1="150" y1="485" x2="200" y2="485" stroke="black" stroke-width="4" />'
    svg += f'<circle cx="175" cy="470" r="12" stroke="red" stroke-width="3" fill="none" />'

    # --- 選手とボール ---
    for name, p in pos.items():
        if name.startswith("R"): color, label_c = "red", "white"
        elif name.startswith("B"): color, label_c = "blue", "white"
        else: color, label_c = "yellow", "black"
        
        r = 8 if name == "Ball" else 13
        stroke = "black" if name == "Ball" else "white"
        
        svg += f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{color}" stroke="{stroke}" stroke-width="2" />'
        label = "B" if name == "Ball" else name
        svg += f'<text x="{p[0]}" y="{p[1]+4}" font-size="10" text-anchor="middle" fill="{label_c}" font-family="Arial" font-weight="bold">{label}</text>'

    svg += '</svg>'
    return svg

st.write("---")
st.components.v1.html(draw_perfect_court(), height=550)
