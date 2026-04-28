import streamlit as st

# ページ設定
st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")

st.title("🏀 バスケ作戦盤 Pro")

# --- 1. 選手とボールの「位置」を記憶する ---
if "positions" not in st.session_state:
    # 初期の配置データ
    st.session_state.positions = {
        "R1": [50, 100], "R2": [120, 100], "R3": [190, 100], "R4": [260, 100], "R5": [310, 100],
        "B1": [50, 400], "B2": [120, 400], "B3": [190, 400], "B4": [260, 400], "B5": [310, 400],
        "Ball": [175, 250]
    }

# --- 2. 操作パネル ---
st.write("### 🕹️ 配置設定")
target = st.selectbox("動かす対象を選んでください:", list(st.session_state.positions.keys()))

col1, col2 = st.columns(2)
with col1:
    x = st.slider("左右の位置 (X)", 0, 350, st.session_state.positions[target][0])
with col2:
    y = st.slider("前後の位置 (Y)", 0, 520, st.session_state.positions[target][1])

# スライダーの値を記憶に反映
st.session_state.positions[target] = [x, y]

# --- 3. コートの描画（SVG方式：これが最も安定して色が出ます） ---
# 画像ファイルを使わず、ブラウザに直接「図形を描け」と命令する方式です。
def draw_svg_court():
    pos = st.session_state.positions
    
    # SVGコードの作成
    svg = f"""
    <svg width="350" height="520" viewBox="0 0 350 520" xmlns="http://www.w3.org/2000/svg">
        <rect width="350" height="520" fill="#FF8C00" />
        
        <rect x="10" y="10" width="330" height="500" fill="none" stroke="white" stroke-width="3" />
        <line x1="10" y1="260" x2="340" y2="260" stroke="white" stroke-width="3" />
        <circle cx="175" cy="260" r="40" fill="none" stroke="white" stroke-width="3" />
        
        <rect x="115" y="10" width="120" height="140" fill="none" stroke="white" stroke-width="3" />
        <rect x="115" y="370" width="120" height="140" fill="none" stroke="white" stroke-width="3" />

        {" ".join([f'<circle cx="{p[0]}" cy="{p[1]}" r="12" fill="red" stroke="white" stroke-width="2" />' for k, p in pos.items() if k.startswith("R")])}
        {" ".join([f'<circle cx="{p[0]}" cy="{p[1]}" r="12" fill="blue" stroke="white" stroke-width="2" />' for k, p in pos.items() if k.startswith("B")])}
        
        <circle cx="{pos['Ball'][0]}" cy="{pos['Ball'][1]}" r="8" fill="orange" stroke="black" stroke-width="2" />
        
        <text x="{pos['Ball'][0]}" y="{pos['Ball'][1]-12}" font-size="10" text-anchor="middle" fill="black">Ball</text>
    </svg>
    """
    return svg

# 4. 描画したSVGを表示
st.write("---")
st.components.v1.html(draw_svg_court(), height=550)

st.success("オレンジのコートが表示され、スライダーで選手が動かせれば完成です！")
