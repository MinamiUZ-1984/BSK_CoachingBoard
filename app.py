import streamlit as st

st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")
st.title("🏀 バスケ作戦盤 Pro")

# --- 1. 選手とボールの位置記憶 ---
if "positions" not in st.session_state:
    st.session_state.positions = {
        "R1": [175, 120], "R2": [50, 180], "R3": [300, 180], "R4": [100, 240], "R5": [250, 240],
        "B1": [175, 400], "B2": [50, 340], "B3": [300, 340], "B4": [100, 280], "B5": [250, 280],
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

# --- 3. コートを描画するSVG関数 (サイズ調整版) ---
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
    
    # センターサークル (半径40)
    svg += f'<circle cx="175" cy="260" r="40" {style} />'

    # --- 上半分のライン ---
    # ペイントエリア: サークル直径(80)に合わせて幅を調整 (175を中心に左右40ずつ)
    svg += f'<rect x="135" y="10" width="80" height="150" {style} />'
    # フリースローサークル: センターサークルと同じ半径40
    svg += f'<circle cx="175" cy="160" r="40" {style} />'
    # 3Pライン
    svg += f'<path d="M 30 10 A 150 150 0 0 0 320 10" {style} />'
    # ゴール
    svg += f'<line x1="150" y1="35" x2="200" y2="35" stroke="black" stroke-width="4" />'
    svg += f'<circle cx="175" cy="50" r="12" stroke="red" stroke-width="3" fill="none" />'

    # --- 下半分のライン ---
    # ペイントエリア
    svg += f'<rect x="135" y="360" width="80" height="150" {style} />'
    # フリースローサークル
    svg += f'<circle cx="175" cy="360" r="40" {style} />'
    # 3Pライン
    svg += f'<path d="M 30 510 A 150 150 0 0 1 320 510" {style} />'
    # ゴール
    svg += f'<line x1="150" y1="485" x2="200" y2="485" stroke="black" stroke-width="4" />'
    svg += f'<circle cx="175" cy="470" r="12" stroke="red" stroke-width="3" fill="none" />'

    # --- 選手とボール ---
    for name, p in pos.items():
        if name.startswith("R"): color, label_c = "red", "white"
        elif name.startswith("B"): color, label_c = "blue", "white"
        else: color, label_c = "yellow", "black" # ボールを見やすく黄色に
        
        r = 8 if name == "Ball" else 13
        stroke = "black" if name == "Ball" else "white"
        
        svg += f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{color}" stroke="{stroke}" stroke-width="2" />'
        label = "B" if name == "Ball" else name
        svg += f'<text x="{p[0]}" y="{p[1]+4}" font-size="10" text-anchor="middle" fill="{label_c}" font-family="Arial" font-weight="bold">{label}</text>'

    svg += '</svg>'
    return svg

st.write("---")
st.components.v1.html(draw_perfect_court(), height=550)
