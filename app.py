import streamlit as st

# ページ設定
st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")

# --- iPhoneの画面幅を使い切るためのCSS魔法 ---
st.markdown("""
    <style>
    /* メインコンテンツの余白を極限まで削る */
    .main .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-top: 1rem !important;
        max-width: 100%;
    }
    /* タイトルの文字サイズを少し調整して場所を稼ぐ */
    h1 {
        font-size: 1.8rem !important;
        text-align: center;
    }
    /* コンポーネントを囲むiframeの横幅を強制100%に */
    iframe {
        width: 100% !important;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 バスケ作戦盤 Pro")

# --- 1. 位置記憶（完璧なレイアウトのまま） ---
if "positions" not in st.session_state:
    st.session_state.positions = {
        "R1": [175, 150], "R2": [60, 200], "R3": [290, 200], "R4": [100, 280], "R5": [250, 280],
        "B1": [175, 370], "B2": [60, 320], "B3": [290, 320], "B4": [100, 240], "B5": [250, 240],
        "Ball": [175, 260]
    }

# --- 2. 操作パネル（スマホで見やすいよう少しコンパクトに） ---
st.write("### 🕹️ 配置設定")
target = st.selectbox("動かす対象:", list(st.session_state.positions.keys()))
col1, col2 = st.columns(2)
with col1:
    st.session_state.positions[target][0] = st.slider("左右 (X)", 0, 350, st.session_state.positions[target][0])
with col2:
    st.session_state.positions[target][1] = st.slider("前後 (Y)", 0, 520, st.session_state.positions[target][1])

# --- 3. 完璧なコート（SVGレスポンシブ版） ---
def draw_perfect_court():
    pos = st.session_state.positions
    c_orange = "#FF8C00"
    c_white = "white"
    
    # 黄金比を維持したまま、表示幅を100%に。最大幅をiPhoneに合わせる。
    svg = f'<svg width="100%" height="auto" viewBox="0 0 350 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 350px; display: block; margin: 0 auto; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">'
    svg += f'<rect width="350" height="520" fill="{c_orange}" />'
    style = f'fill="none" stroke="{c_white}" stroke-width="3"'
    
    # 外枠・センター
    svg += f'<rect x="10" y="10" width="330" height="500" {style} />'
    svg += f'<line x1="10" y1="260" x2="340" y2="260" {style} />'
    svg += f'<circle cx="175" cy="260" r="40" {style} />'

    def create_half_court(is_top):
        offset_y = 10 if is_top else 510
        direction = 1 if is_top else -1
        h_svg = ""
        p_y = offset_y if is_top else offset_y - 110
        h_svg += f'<rect x="135" y="{p_y}" width="80" height="110" {style} />'
        fs_cy = offset_y + (110 * direction)
        h_svg += f'<circle cx="175" cy="{fs_cy}" r="40" {style} />'
        line_len = 15
        line_end_y = offset_y + (line_len * direction)
        h_svg += f'<line x1="30" y1="{offset_y}" x2="30" y2="{line_end_y}" {style} />'
        h_svg += f'<line x1="320" y1="{offset_y}" x2="320" y2="{line_end_y}" {style} />'
        sweep = 0 if is_top else 1
        h_svg += f'<path d="M 30 {line_end_y} A 145 145 0 0 {sweep} 320 {line_end_y}" {style} />'
        g_y = offset_y + (40 * direction)
        board_y = offset_y + (25 * direction)
        h_svg += f'<line x1="150" y1="{board_y}" x2="200" y2="{board_y}" stroke="black" stroke-width="4" />'
        h_svg += f'<circle cx="175" cy="{g_y}" r="12" stroke="red" stroke-width="3" fill="none" />'
        return h_svg

    svg += create_half_court(is_top=True)
    svg += create_half_court(is_top=False)

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

# --- 4. 表示実行 ---
st.write("---")
# 中央寄せするためのコンテナ
st.components.v1.html(
    f"""
    <div style="width: 100%; display: flex; justify-content: center; align-items: flex-start; background-color: transparent;">
        {draw_perfect_court()}
    </div>
    """,
    height=540
)

st.caption("iPhone 15用に表示を最適化しました。端まで綺麗に見えていますか？")
