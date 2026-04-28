import streamlit as st

# 1. ページ設定
st.set_page_config(page_title="バスケ作戦盤 Pro", layout="centered")

# iPhone 15 最適化CSS
st.markdown("""
    <style>
    .main .block-container {
        padding-left: 0.1rem !important;
        padding-right: 0.1rem !important;
        padding-top: 0.5rem !important;
        max-width: 100% !important;
    }
    iframe { width: 100% !important; border: none; min-height: 700px; }
    h1 { font-size: 1.5rem !important; text-align: center; margin-bottom: 0.2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 バスケ作戦盤 Pro")

# 表示範囲の切り替え
view_range = st.radio("表示範囲", ["フル", "上半面", "下半面"], horizontal=True)

# --- 2. 統合操作エンジン (選手移動 + お絵かき履歴一括管理) ---
def draw_unified_board(view):
    c_orange = "#FF8C00"
    c_white = "white"
    
    # 表示範囲設定
    if view == "上半面": v_box, h_val = "0 0 350 260", 430
    elif view == "下半面": v_box, h_val = "0 260 350 260", 430
    else: v_box, h_val = "0 0 350 520", 630

    # 初期配置データ（JSに渡す用）
    initial_pos = {
        "R1": [175, 185], "R2": [70, 140], "R3": [280, 140], "R4": [35, 50], "R5": [315, 50],
        "B1": [175, 150], "B2": [105, 115], "B3": [245, 115], "B4": [55, 65], "B5": [295, 65],
        "Ball": [175, 210]
    }

    svg_html = f"""
    <div id="wrapper" style="width: 100%; max-width: 390px; margin: 0 auto; user-select: none;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px; gap: 5px;">
            <button id="modeBtn" style="flex: 2; padding: 10px; border-radius: 5px; border: 1px solid #ccc; background: #eee; font-weight: bold; font-size: 14px;">🖐️ 移動</button>
            <button id="undoBtn" style="flex: 1; padding: 10px; border-radius: 5px; border: 1px solid #ccc; background: #fff; font-size: 18px;">↩️</button>
            <button id="redoBtn" style="flex: 1; padding: 10px; border-radius: 5px; border: 1px solid #ccc; background: #fff; font-size: 18px;">↪️</button>
            <button id="resetAllBtn" style="flex: 1.5; padding: 10px; border-radius: 5px; border: 1px solid #ccc; background: #ffcccc; color: red; font-weight: bold; font-size: 14px;">🔄 初期化</button>
        </div>

        <svg id="court-svg" width="100%" viewBox="{v_box}" xmlns="http://www.w3.org/2000/svg" 
             style="display: block; touch-action: none; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); background: {c_orange};">
            
            <g fill="none" stroke="{c_white}" stroke-width="3" pointer-events="none">
                <rect x="10" y="10" width="330" height="500" />
                <line x1="10" y1="260" x2="340" y2="260" />
                <circle cx="175" cy="260" r="40" />
                <rect x="120" y="10" width="110" height="110" />
                <circle cx="175" cy="120" r="40" />
                <line x1="30" y1="10" x2="30" y2="25" /><line x1="320" y1="10" x2="320" y2="25" />
                <path d="M 30 25 A 145 145 0 0 0 320 25" />
                <line x1="150" y1="35" x2="200" y2="35" stroke="black" stroke-width="4" />
                <circle cx="175" cy="50" r="12" stroke="red" stroke-width="3" fill="none" />
                <rect x="120" y="400" width="110" height="110" />
                <circle cx="175" cy="400" r="40" />
                <line x1="30" y1="510" x2="30" y2="495" /><line x1="320" y1="510" x2="320" y2="495" />
                <path d="M 30 495 A 145 145 0 0 1 320 495" />
                <line x1="150" y1="485" x2="200" y2="485" stroke="black" stroke-width="4" />
                <circle cx="175" cy="470" r="12" stroke="red" stroke-width="3" fill="none" />
            </g>

            <g id="draw-layer" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"></g>

            <g id="players-layer">
            { "".join([f'''
            <g class="draggable" id="{k}" transform="translate({p[0]},{p[1]})" style="cursor: move;">
                <circle r="{"10" if k=="Ball" else "17"}" fill="{"yellow" if k=="Ball" else ("red" if k.startswith("R") else "#1E90FF")}" stroke="{"black" if k=="Ball" else "white"}" stroke-width="2" />
                <text dy=".3em" font-size="11" text-anchor="middle" fill="{"black" if k=="Ball" else "white"}" font-family="Arial" font-weight="bold" pointer-events="none">{"B" if k=="Ball" else k}</text>
            </g>
            ''' for k, p in initial_pos.items()]) }
            </g>
        </svg>
    </div>

    <script>
        const svg = document.getElementById('court-svg');
        const drawLayer = document.getElementById('draw-layer');
        const modeBtn = document.getElementById('modeBtn');
        const undoBtn = document.getElementById('undoBtn');
        const redoBtn = document.getElementById('redoBtn');
        const resetBtn = document.getElementById('resetAllBtn');

        const initialPos = {str(initial_pos)};
        let isDrawingMode = false;
        let isDrawing = false;
        let currentPath = null;
        
        let selectedElement = null;
        let startPos = {{x: 0, y: 0}};
        let offset = {{x: 0, y: 0}};

        // 共通履歴スタック（線も移動もここに入る）
        let history = [];
        let redoStack = [];

        // モード切替
        modeBtn.addEventListener('click', () => {{
            isDrawingMode = !isDrawingMode;
            modeBtn.innerText = isDrawingMode ? "✏️ 描画中" : "🖐️ 移動中";
            modeBtn.style.background = isDrawingMode ? "#ffffcc" : "#eee";
        }});

        function getMousePosition(evt) {{
            const CTM = svg.getScreenCTM();
            if (evt.touches) evt = evt.touches[0];
            return {{ x: (evt.clientX - CTM.e) / CTM.a, y: (evt.clientY - CTM.f) / CTM.d }};
        }}

        svg.addEventListener('mousedown', start);
        svg.addEventListener('mousemove', move);
        svg.addEventListener('mouseup', end);
        svg.addEventListener('touchstart', start, {{passive: false}});
        svg.addEventListener('touchmove', move, {{passive: false}});
        svg.addEventListener('touchend', end);

        function start(evt) {{
            const pos = getMousePosition(evt);
            if (isDrawingMode) {{
                isDrawing = true;
                currentPath = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
                currentPath.setAttribute("points", `${{pos.x}},${{pos.y}}`);
                drawLayer.appendChild(currentPath);
            }} else {{
                const target = evt.target.closest('.draggable');
                if (target) {{
                    selectedElement = target;
                    const translate = selectedElement.transform.baseVal.getItem(0);
                    startPos = {{x: translate.matrix.e, y: translate.matrix.f}}; // 開始地点を記録
                    offset = {{x: pos.x - startPos.x, y: pos.y - startPos.y}};
                }}
            }}
            if (evt.type === 'touchstart' && (isDrawingMode || selectedElement)) evt.preventDefault();
        }}

        function move(evt) {{
            const pos = getMousePosition(evt);
            if (isDrawingMode && isDrawing) {{
                let pts = currentPath.getAttribute("points");
                currentPath.setAttribute("points", pts + ` ${{pos.x}},${{pos.y}}`);
            }} else if (selectedElement) {{
                selectedElement.setAttribute('transform', `translate(${{pos.x - offset.x}}, ${{pos.y - offset.y}})`);
            }}
            if (evt.touches && (isDrawingMode || selectedElement)) evt.preventDefault();
        }}

        function end() {{
            if (isDrawing) {{
                history.push({{ type: 'path', element: currentPath }});
                redoStack = [];
                isDrawing = false;
            }} else if (selectedElement) {{
                const translate = selectedElement.transform.baseVal.getItem(0);
                const endPos = {{x: translate.matrix.e, y: translate.matrix.f}};
                
                // 実際に動いた場合のみ履歴に追加
                if (Math.abs(startPos.x - endPos.x) > 1 || Math.abs(startPos.y - endPos.y) > 1) {{
                    history.push({{
                        type: 'move',
                        id: selectedElement.id,
                        from: startPos,
                        to: endPos
                    }});
                    redoStack = [];
                }}
                selectedElement = null;
            }}
        }}

        // ↩️ 戻る（統合Undo）
        undoBtn.addEventListener('click', () => {{
            if (history.length === 0) return;
            const action = history.pop();
            redoStack.push(action);

            if (action.type === 'path') {{
                drawLayer.removeChild(action.element);
            }} else if (action.type === 'move') {{
                const el = document.getElementById(action.id);
                el.setAttribute('transform', `translate(${{action.from.x}}, ${{action.from.y}})`);
            }}
        }});

        // ↪️ 進む（統合Redo）
        redoBtn.addEventListener('click', () => {{
            if (redoStack.length === 0) return;
            const action = redoStack.pop();
            history.push(action);

            if (action.type === 'path') {{
                drawLayer.appendChild(action.element);
            }} else if (action.type === 'move') {{
                const el = document.getElementById(action.id);
                el.setAttribute('transform', `translate(${{action.to.x}}, ${{action.to.y}})`);
            }}
        }});

        // 🔄 初期化（全クリア & 選手リセット）
        resetBtn.addEventListener('click', () => {{
            if (!confirm("すべてリセットして初期配置に戻しますか？")) return;
            drawLayer.innerHTML = "";
            for (let id in initialPos) {{
                const el = document.getElementById(id);
                if (el) el.setAttribute('transform', `translate(${{initialPos[id][0]}}, ${{initialPos[id][1]}})`);
            }}
            history = [];
            redoStack = [];
        }});
    </script>
    """
    return svg_html

# --- 3. 表示 ---
st.components.v1.html(draw_unified_board(view_range), height=700)
