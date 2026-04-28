import streamlit as st

# 1. ページ設定
st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")

# --- iPhone 15 画面使い切りCSS魔法（余白を極限までカット） ---
st.markdown("""
    <style>
    /* メインコンテンツの余白をさらに削る */
    .main .block-container {
        padding-left: 0.2rem !important;
        padding-right: 0.2rem !important;
        padding-top: 0.5rem !important;
        max-width: 100%;
    }
    h1 {
        font-size: 1.6rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    iframe {
        width: 100% !important;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 バスケ作戦盤 Pro")

# --- 2. 復活した黄金レイアウト + ドラッグ機能の大改造 ---
def draw_perfect_interactive_court():
    c_orange = "#FF8C00"
    c_white = "white"
    
    # 初期の配置（広く使いやすくなった黄金比）
    players = [
        {"id": "R1", "x": 175, "y": 150, "color": "red"},
        {"id": "R2", "x": 60, "y": 200, "color": "red"},
        {"id": "R3", "x": 290, "y": 200, "color": "red"},
        {"id": "R4", "x": 100, "y": 280, "color": "red"},
        {"id": "R5", "x": 250, "y": 280, "color": "red"},
        {"id": "B1", "x": 175, "y": 370, "color": "blue"},
        {"id": "B2", "x": 60, "y": 320, "color": "blue"},
        {"id": "B3", "x": 290, "y": 320, "color": "blue"},
        {"id": "B4", "x": 100, "y": 240, "color": "blue"},
        {"id": "B5", "x": 250, "y": 240, "color": "blue"},
        {"id": "Ball", "x": 175, "y": 260, "color": "yellow"}
    ]

    # --- 修正ポイント1：コート全体のサイズアップ ---
    # viewBox="0 0 350 520" は変えず、max-widthを380pxまで上げることでiPhone 15の横幅をほぼ使い切ります。
    svg_html = f"""
    <svg id="court" width="100%" height="auto" viewBox="0 0 350 520" xmlns="http://www.w3.org/2000/svg" 
         style="max-width: 380px; display: block; margin: 0 auto; touch-action: none; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
        
        <rect width="350" height="520" fill="{c_orange}" />
        <g fill="none" stroke="{c_white}" stroke-width="3">
            <rect x="10" y="10" width="330" height="500" />
            <line x1="10" y1="260" x2="340" y2="260" />
            <circle cx="175" cy="260" r="40" />
            
            <rect x="135" y="10" width="80" height="110" /> <circle cx="175" cy="120" r="40" /> <line x1="30" y1="10" x2="30" y2="25" />
            <line x1="320" y1="10" x2="320" y2="25" />
            <path d="M 30 25 A 145 145 0 0 0 320 25" />
            
            <rect x="135" y="410" width="80" height="110" />
            <circle cx="175" cy="400" r="40" />
            <line x1="30" y1="510" x2="30" y2="495" />
            <line x1="320" y1="510" x2="320" y2="495" />
            <path d="M 30 495 A 145 145 0 0 1 320 495" />
        </g>
        
        <line x1="150" y1="35" x2="200" y2="35" stroke="black" stroke-width="4" />
        <circle cx="175" cy="50" r="12" stroke="red" stroke-width="3" fill="none" />
        <line x1="150" y1="485" x2="200" y2="485" stroke="black" stroke-width="4" />
        <circle cx="175" cy="470" r="12" stroke="red" stroke-width="3" fill="none" />

        { "".join([f'''
        <g class="draggable" id="{p['id']}" transform="translate({p['x']},{p['y']})" style="cursor: move;">
            <circle r="{"10" if p['id']=="Ball" else "17"}" fill="{p['color']}" stroke="{"black" if p['id']=="Ball" else "white"}" stroke-width="2" />
            <text dy=".3em" font-size="11" text-anchor="middle" fill="{"black" if p['id']=="Ball" else "white"}" font-family="Arial" font-weight="bold" pointer-events="none">
                {"B" if p['id']=="Ball" else p['id']}
            </text>
        </g>
        ''' for p in players]) }

        <script>
            // （前回のJavaScriptドラッグ処理をそのまま活用）
            const svg = document.getElementById('court');
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
                if (evt.touches) {{ evt = evt.touches[0]; }}
                return {{ x: (evt.clientX - CTM.e) / CTM.a, y: (evt.clientY - CTM.f) / CTM.d }};
            }}
            function startDrag(evt) {{
                const target = evt.target.closest('.draggable');
                if (target) {{
                    selectedElement = target;
                    const pos = getMousePosition(evt);
                    const transforms = selectedElement.transform.baseVal;
                    if (transforms.length === 0 || transforms.getItem(0).type !== SVGTransform.SVG_TRANSFORM_TRANSLATE) {{
                        selectedElement.setAttribute('transform', 'translate(0,0)');
                    }}
                    const translate = transforms.getItem(0);
                    offset.x = pos.x - translate.matrix.e; offset.y = pos.y - translate.matrix.f;
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
    </svg>
    """
    return svg_html

# --- 3. 画面表示 ---
st.write("選手やボールを指で動かしてください。")

# htmlコンポーネントの中で中央寄せ。高さもiPhoneに合わせて微調整。
st.components.v1.html(
    f"""
    <div style="width: 100%; display: flex; justify-content: center; background-color: transparent;">
        {draw_perfect_interactive_court()}
    </div>
    """,
    height=545
)

if st.button("配置をリセット"):
    st.rerun()

st.caption("※iPhone 15 完全対応版。操作性とレイアウトを修正しました。")
