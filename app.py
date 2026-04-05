import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(
    page_title="Data Analytics Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    #MainMenu, footer, header { visibility: hidden; }
    .stApp { background: #020617 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# ── 读取密码（仅从 Streamlit Secrets，不含任何默认值）─────────
try:
    CORRECT_PASSWORD = st.secrets["password"]
except Exception:
    st.error("⚠️ 未配置访问密码，请在 Streamlit Cloud → Secrets 中设置 `password`")
    st.stop()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── 登录页：弹窗动画（纯视觉）+ 服务端校验 ───────────────────
if not st.session_state.authenticated:

    # 弹窗：fixed 定位真居中 + 液态玻璃效果
    st.markdown("""
    <style>
      /* ── 全屏背景覆盖 ── */
      .login-overlay {
        position: fixed;
        inset: 0;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(ellipse at 30% 20%, rgba(13,148,136,0.18) 0%, transparent 55%),
                    radial-gradient(ellipse at 75% 80%, rgba(99,102,241,0.15) 0%, transparent 50%),
                    linear-gradient(135deg, #020617 0%, #0b1120 50%, #0f172a 100%);
        pointer-events: none;
      }

      /* ── 玻璃弹窗 ── */
      .glass-modal {
        pointer-events: all;
        position: relative;
        width: 320px;
        padding: 40px 32px 32px;
        border-radius: 28px;
        overflow: hidden;

        /* 玻璃基底 */
        background:
          linear-gradient(140deg,
            rgba(255,255,255,0.09) 0%,
            rgba(45,212,191,0.04) 40%,
            rgba(99,102,241,0.06) 100%);
        backdrop-filter: blur(28px) saturate(160%);
        -webkit-backdrop-filter: blur(28px) saturate(160%);

        /* 液态边框：渐变描边 */
        border: 1px solid transparent;
        background-clip: padding-box;
        box-shadow:
          0 0 0 1px rgba(45,212,191,0.25),
          inset 0 1px 0 rgba(255,255,255,0.12),
          0 8px 32px rgba(0,0,0,0.55),
          0 0 80px rgba(45,212,191,0.08),
          0 0 120px rgba(99,102,241,0.06);

        animation: popIn .4s cubic-bezier(.34,1.56,.64,1) both;
      }

      /* 流光扫过伪元素 */
      .glass-modal::before {
        content: '';
        position: absolute;
        top: -60%;
        left: -60%;
        width: 220%;
        height: 220%;
        background: conic-gradient(
          from 200deg at 50% 50%,
          transparent 0deg,
          rgba(45,212,191,0.06) 60deg,
          rgba(255,255,255,0.04) 80deg,
          transparent 120deg
        );
        animation: spin 6s linear infinite;
        pointer-events: none;
      }

      /* 顶部高光条 */
      .glass-modal::after {
        content: '';
        position: absolute;
        top: 0; left: 10%; right: 10%;
        height: 1px;
        background: linear-gradient(90deg,
          transparent, rgba(255,255,255,0.35), transparent);
        border-radius: 50%;
      }

      @keyframes popIn {
        from { opacity:0; transform:scale(0.72) translateY(16px); filter:blur(4px); }
        to   { opacity:1; transform:scale(1)   translateY(0);     filter:blur(0); }
      }
      @keyframes spin {
        to { transform: rotate(360deg); }
      }

      /* ── 把 Streamlit 原生控件移入弹窗后的样式 ── */
      .glass-modal .stTextInput input {
        background: rgba(0,0,0,0.35) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(45,212,191,0.28) !important;
        border-radius: 12px !important;
        text-align: center !important;
        font-size: 15px !important;
        letter-spacing: 2px;
        transition: border-color .2s, box-shadow .2s !important;
        backdrop-filter: blur(6px);
      }
      .glass-modal .stTextInput input::placeholder { letter-spacing:0; color:#475569; }
      .glass-modal .stTextInput input:focus {
        border-color: #2dd4bf !important;
        box-shadow: 0 0 0 3px rgba(45,212,191,0.18), 0 0 20px rgba(45,212,191,0.1) !important;
      }
      .glass-modal .stButton > button {
        background: linear-gradient(90deg, #0d9488, #2dd4bf) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 12px 0 !important;
        width: 100%;
        letter-spacing: .5px;
        box-shadow: 0 4px 24px rgba(45,212,191,0.25) !important;
        transition: opacity .2s, transform .15s !important;
      }
      .glass-modal .stButton > button:hover  { opacity:.88 !important; transform:translateY(-1px); }
      .glass-modal .stButton > button:active { transform:scale(.97); }

      /* 隐藏弹窗外的 Streamlit 输入（fallback 用） */
      section.main > div > div > div[data-testid="stTextInput"],
      section.main > div > div > div[data-testid="stButton"] {
        display: none !important;
      }
    </style>

    <div class="login-overlay">
      <div class="glass-modal" id="modal-anchor"></div>
    </div>
    """, unsafe_allow_html=True)

    # JS：将 Streamlit 原生输入移入玻璃弹窗
    st.markdown("""
    <script>
      (function move() {
        const anchor = document.getElementById('modal-anchor');
        const inputs = document.querySelectorAll(
          'section.main [data-testid="stTextInput"], section.main [data-testid="stButton"]'
        );
        if (anchor && inputs.length >= 2) {
          inputs.forEach(el => {
            el.style.display = 'block';
            anchor.appendChild(el);
          });
        } else {
          setTimeout(move, 40);
        }
      })();
    </script>
    """, unsafe_allow_html=True)


    pwd = st.text_input("密码", type="password",
                        placeholder="请输入访问密码",
                        label_visibility="collapsed")
    btn = st.button("进入系统 →", use_container_width=True, type="primary")

    if btn or pwd:
        if pwd == CORRECT_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        elif pwd:
            st.error("密码错误，请重试")

# ── 已认证：全屏嵌入 HTML ─────────────────────────────────────
else:
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=5000, scrolling=True)
