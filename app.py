import streamlit as st

# 1. ページ設定
st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")

# iPhone 15 画面使い切りCSS（余白を最小限に）
st.markdown("""
    <style>
    .main .block-container {
        padding-left: 0.1rem !important;
        padding-right: 0.1rem !important;
        padding-top: 0.5rem !important;
    }
    iframe {
        width: 100% !important;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 バスケ作戦盤 Pro")

# --- 2. 選手・ボールの初期配置（5ポジション固定） ---
if "positions" not in st.session_state:
    st.session_state.positions = {
        "R1": [175, 175], "R2": [75, 130], "R3": [275, 130], "R4": [35, 45], "R5": [315, 45],
        "B1": [175, 345], "B2": [75, 390], "B3": [275, 390], "B4": [35, 475], "B5": [315, 475],
        "Ball": [175, 260]
    }

# --- 3. 表示設定（ズームスライダーを廃止し、範囲切替のみに） ---
col_v1, col_v2 = st.columns([3, 1])
with col_v1:
    view_mode = st.radio("表示範囲", ["フル", "上半面", "下半面"], horizontal=True)
with col_v2:
    if st.button("リセット"):
        st.session_state.clear()
        st.rerun()

# --- 4. 拡大機能付きSVG描画 ---
def draw_expandable_court(view):
    c_orange = "#FF8C00"
    c_white = "white"
    
    # 表示範囲設定
    if view == "上半面": v_box, h_val = "0 0 350 260", 350
    elif view == "下半面": v_box, h_val = "0 260 350 260", 350
    else: v_box, h_val = "0 0 350 520", 550

    svg_html = f"""
    <div id="court-container" style="position: relative; width: 100%; max-width: 350px; margin: 0 auto; transition: max-width 0.3s ease;">
        <div id="expand-btn" style="position: absolute; top: 15px; right: 15px; z-index: 10; background: rgba(0,0,0,0.5); border-radius: 4px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: white; font-size: 20px;">
            ⛶
        </div>

        <svg id="court-svg" width="100%" viewBox="{v_box}" xmlns="http://www.w3.org/2000/svg" 
             style="display: block; touch-action: none; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
            
            <rect width="350" height="520" fill="{c_orange}" />
            
            <g fill="none" stroke="{c_white}" stroke-width="3">
                <rect x="10" y="10" width="330" height="500" />
                <line x1="10" y1="260" x2="340" y2="260" />
                <circle cx="175" cy="260" r="40" />
                <rect x="135" y="10" width="80" height="110" />
                <circle cx="175" cy="120" r="40" />
                <line x1="30" y1="10" x2="30" y2="25" /><line x1="320" y1="10" x2="320" y2="25" />
                <path d="M 30 25 A 145 145 0 0 0 320 25" />
                <rect x="135" y="410" width="80" height="110" />
                <circle cx="175" cy="400" r="40" />
                <line x1="30" y1="510" x2="30" y2="495" /><line x1="320" y1="510" x2="320" y2="495" />
                <path d="M 30 495 A 145 145 0 0 1 320 495" />
            </g>
            
            <g stroke-width="4" stroke="black"><line x1="150" y1="35" x2="200" y2="35" /><line x1="150" y1="485" x2="200" y2="485" /></g>
            <circle cx="175" cy="50" r="12" stroke="red" stroke-width="3" fill="none" />
            <circle cx="175" cy="470" r="12" stroke="red" stroke-width="3" fill="none" />

            { "".join([f'''
            <g class="draggable" id="{k}" transform="translate({p[0]},{p[1]})" style="cursor: move;">
                <circle r="{"10" if k=="Ball" else "17"}" fill="{"yellow" if k=="Ball" else ("red" if k.startswith("R") else "blue")}" stroke="{"black" if k=="Ball" else "white"}" stroke-width="2" />
                <text dy=".3em" font-size="11" text-anchor="middle" fill="{"black" if k=="Ball" else "white"}" font-family="Arial" font-weight="bold" pointer-events="none">
                    {"B" if k=="Ball" else k}
                </text>
            </g>
            ''' for k, p in st.session_state.positions.items()]) }
        </svg>
    </div>

    <script>
        const container = document.getElementById('court-container');
        const expandBtn = document.getElementById('expand-btn');
        const svg = document.getElementById('court-svg');
        let isExpanded = false;

        // 拡大・縮小の切り替えロジック
        expandBtn.addEventListener('click', () => {{
            isExpanded = !isExpanded;
            if (isExpanded) {{
                container.style.maxWidth = '100%';
                expandBtn.innerText = '⛶'; // ✥ の代わりのアイコン
                expandBtn.style.background = 'rgba(255,0,0,0.6)'; // 拡大中は色を変えて強調
            }} else {{
                container.style.maxWidth = '350px';
                expandBtn.innerText = '⛶';
                expandBtn.style.background = 'rgba(0,0,0,0.5)';
            }}
        }});

        // ドラッグ処理（前回同様）
        let selectedElement = null;
        let offset = {{ x: 0, y: 0 }};
        svg.addEventListener('mousedown', startDrag);
        svg.addEventListener('mousemove', drag);
        svg.addEventListener('mouseup', endDrag);
        svg.addEventListener('touchstart', startDrag, {{passive: false}});
        svg.addEventListener('touchmove', drag, {{passive: false}});
        svg.addEventListener('touchend', endDrag);

        function getMousePosition(evt) {{
            const CTM = svg.getScreenCTM();
            if (evt.touches) evt = evt.touches[0];
            return {{ x: (evt.clientX - CTM.e) / CTM.a, y: (evt.clientY - CTM.f) / CTM.d }};
        }}
        function startDrag(evt) {{
            const target = evt.target.closest('.draggable');
            if (target) {{
                selectedElement = target;
                const pos = getMousePosition(evt);
                const translate = selectedElement.transform.baseVal.getItem(0);
                offset.x = pos.x - translate.matrix.e;
                offset.y = pos.y - translate.matrix.f;
                if (evt.type === 'touchstart') evt.preventDefault();
            }}
        }}
        function drag(evt) {{
            if (selectedElement) {{
                const pos = getMousePosition(evt);
                selectedElement.setAttribute('transform', `translate(${{pos.x - offset.x}}, ${{pos.y - offset.y}})`);
                if (evt.type === 'touchmove') evt.preventDefault();
            }}
        }}
        function endDrag(evt) {{ selectedElement = null; }}
    </script>
    """
    return svg_html, h_val

# --- 5. 表示実行 ---
svg_code, h_val = draw_expandable_court(view_mode)

st.components.v1.html(
    f'<div style="width: 100%; display: flex; justify-content: center; background-color: transparent;">{svg_code}</div>',
    height=h_val + 50
)
