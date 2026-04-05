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

    # 弹出动画容器（不含密码，安全）
    st.markdown("""
    <style>
      @keyframes popIn {
        from { opacity:0; transform:scale(0.65); }
        to   { opacity:1; transform:scale(1); }
      }
      .login-wrap {
        display: flex;
        justify-content: center;
        padding-top: 18vh;
      }
      .login-modal {
        background: rgba(15,23,42,0.95);
        border: 1px solid rgba(45,212,191,0.3);
        border-radius: 20px;
        padding: 36px 32px 28px;
        width: 300px;
        box-shadow: 0 0 60px rgba(45,212,191,0.12), 0 20px 40px rgba(0,0,0,0.7);
        backdrop-filter: blur(20px);
        animation: popIn .35s cubic-bezier(.34,1.56,.64,1) both;
      }
      /* 输入框深色 */
      .stTextInput input {
        background: rgba(0,0,0,0.4) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(45,212,191,0.3) !important;
        border-radius: 10px !important;
        text-align: center !important;
        font-size: 15px !important;
        letter-spacing: 2px;
      }
      .stTextInput input::placeholder { letter-spacing: 0; }
      .stTextInput input:focus {
        border-color: #2dd4bf !important;
        box-shadow: 0 0 0 3px rgba(45,212,191,0.15) !important;
      }
      /* 按钮 */
      .stButton > button {
        background: linear-gradient(90deg, #0d9488, #2dd4bf) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 11px 0 !important;
        width: 100%;
        transition: opacity .2s;
      }
      .stButton > button:hover { opacity: .88; }
    </style>
    <div class="login-wrap">
      <div class="login-modal" id="modal-anchor"></div>
    </div>
    """, unsafe_allow_html=True)

    # 使用 JS 把 Streamlit 原生组件"移入"弹窗动画容器
    st.markdown("""
    <script>
      (function move() {
        const anchor = document.getElementById('modal-anchor');
        const inputs = document.querySelectorAll('[data-testid="stTextInput"], [data-testid="stButton"]');
        if (anchor && inputs.length >= 2) {
          inputs.forEach(el => anchor.appendChild(el));
        } else {
          setTimeout(move, 50);
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
