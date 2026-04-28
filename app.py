import streamlit as st

st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")
st.title("🏀 バスケ作戦盤 Pro")

# --- 1. 選手とボールの位置記憶 ---
if "positions" not in st.session_state:
    st.session_state.positions = {
        "R1": [175, 100], "R2": [60, 150], "R3": [290, 150], "R4": [100, 220], "R5": [250, 220],
        "B1": [175, 420], "B2": [60, 370], "B3": [290, 370], "B4": [100, 300], "B5": [250, 300],
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

# --- 3. 完全線対称を描画するSVG関数 ---
def draw_perfect_court():
    pos = st.session_state.positions
    c_orange = "#FF8C00"
    c_white = "white"
    
    WIDTH, HEIGHT = 350, 520
    CENTER_X, CENTER_Y = WIDTH / 2, HEIGHT / 2
    
    svg = f'<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">'
    svg += f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{c_orange}" />'
    style = f'fill="none" stroke="{c_white}" stroke-width="3"'
    
    # センターライン・外枠・センターサークル
    svg += f'<rect x="10" y="10" width="330" height="500" {style} />'
    svg += f'<line x1="10" y1="{CENTER_Y}" x2="340" y2="{CENTER_Y}" {style} />'
    svg += f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="40" {style} />'

    def create_half_court(is_top):
        offset_y = 10 if is_top else 510
        direction = 1 if is_top else -1
        
        h_svg = ""
        # ペイントエリア (高さを110に固定)
        p_y = offset_y if is_top else offset_y - 110
        h_svg += f'<rect x="135" y="{p_y}" width="80" height="110" {style} />'
        
        # フリースローサークル
        fs_cy = offset_y + (110 * direction)
        h_svg += f'<circle cx="{CENTER_X}" cy="{fs_cy}" r="40" {style} />'
        
        # --- 3Pラインの位置調整 ---
        # センターサークルに被らないよう、直線の長さを「90」から「50」に短縮
        line_len = 50
        line_end_y = offset_y + (line_len * direction)
        
        # 垂直な直線部分
        h_svg += f'<line x1="30" y1="{offset_y}" x2="30" y2="{line_end_y}" {style} />'
        h_svg += f'<line x1="320" y1="{offset_y}" x2="320" y2="{line_end_y}" {style} />'
        
        # 円弧部分 (半径145を維持しつつ、接続点を浅くしたことで全体がゴール側へシフト)
        sweep = 0 if is_top else 1
        h_svg += f'<path d="M 30 {line_end_y} A 145 145 0 0 {sweep} 320 {line_end_y}" {style} />'
        
        # ゴール
        g_y = offset_y + (40 * direction)
        board_y = offset_y + (25 * direction)
        h_svg += f'<line x1="150" y1="{board_y}" x2="200" y2="{board_y}" stroke="black" stroke-width="4" />'
        h_svg += f'<circle cx="{CENTER_X}" cy="{g_y}" r="12" stroke="red" stroke-width="3" fill="none" />'
        
        return h_svg

    svg += create_half_court(is_top=True)
    svg += create_half_court(is_top=False)

    # 選手とボール
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
