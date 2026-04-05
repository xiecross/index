import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(
    page_title="Data Analytics Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 隐藏 Streamlit 默认 UI + 全屏深色背景
st.markdown("""
<style>
  #MainMenu, footer, header { visibility: hidden; }
  .stApp {
    background:
      radial-gradient(ellipse at 25% 15%, rgba(13,148,136,0.22) 0%, transparent 50%),
      radial-gradient(ellipse at 78% 80%, rgba(99,102,241,0.18) 0%, transparent 50%),
      linear-gradient(135deg, #020617 0%, #0b1120 50%, #0f172a 100%) !important;
  }
  .block-container { padding-top: 0 !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# 读取密码（仅从 Streamlit Secrets）
try:
    CORRECT_PASSWORD = st.secrets["password"]
except Exception:
    st.error("⚠️ 请在 Streamlit Cloud → Secrets 中设置 `password`")
    st.stop()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── 登录页 ─────────────────────────────────────────────────────
if not st.session_state.authenticated:

    # 垂直居中：顶部留白
    st.markdown("<div style='height:28vh'></div>", unsafe_allow_html=True)

    # 三列居中
    _, col, _ = st.columns([1, 1, 1])
    with col:
        # 玻璃卡片包裹层（开）
        st.markdown("""
        <style>
          /* 弹出动画 */
          @keyframes popIn {
            from { opacity:0; transform:scale(0.72) translateY(18px); filter:blur(5px); }
            to   { opacity:1; transform:scale(1)    translateY(0);    filter:blur(0);   }
          }
          /* 流光旋转 */
          @keyframes shimmer {
            0%   { background-position: -200% center; }
            100% { background-position:  200% center; }
          }

          /* 卡片本体 */
          div[data-testid="column"]:nth-child(2) > div:first-child {
            position: relative;
            border-radius: 28px !important;
            padding: 40px 32px 36px !important;
            overflow: hidden;

            background:
              linear-gradient(140deg,
                rgba(255,255,255,0.08) 0%,
                rgba(45,212,191,0.05) 45%,
                rgba(99,102,241,0.07) 100%);
            backdrop-filter: blur(32px) saturate(180%);
            -webkit-backdrop-filter: blur(32px) saturate(180%);

            box-shadow:
              0 0 0 1px rgba(45,212,191,0.28),
              inset 0 1px 0 rgba(255,255,255,0.14),
              0 12px 40px rgba(0,0,0,0.6),
              0 0 90px rgba(45,212,191,0.10),
              0 0 130px rgba(99,102,241,0.07);

            animation: popIn .45s cubic-bezier(.34,1.56,.64,1) both;
          }

          /* 顶部高光线 */
          div[data-testid="column"]:nth-child(2) > div:first-child::after {
            content: '';
            position: absolute;
            top: 0; left: 10%; right: 10%; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
          }

          /* 流光层 */
          div[data-testid="column"]:nth-child(2) > div:first-child::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(105deg,
              transparent 30%,
              rgba(255,255,255,0.04) 50%,
              transparent 70%);
            background-size: 200% 100%;
            animation: shimmer 4s ease infinite;
            pointer-events: none;
          }

          /* 输入框 */
          div[data-testid="column"]:nth-child(2) .stTextInput input {
            background: rgba(0,0,0,0.38) !important;
            color: #f1f5f9 !important;
            border: 1px solid rgba(45,212,191,0.30) !important;
            border-radius: 12px !important;
            text-align: center !important;
            font-size: 15px !important;
            letter-spacing: 2px;
            transition: border-color .2s, box-shadow .2s !important;
          }
          div[data-testid="column"]:nth-child(2) .stTextInput input::placeholder {
            letter-spacing: 0; color: #475569;
          }
          div[data-testid="column"]:nth-child(2) .stTextInput input:focus {
            border-color: #2dd4bf !important;
            box-shadow: 0 0 0 3px rgba(45,212,191,0.20),
                        0 0 24px rgba(45,212,191,0.12) !important;
          }

          /* 按钮 */
          div[data-testid="column"]:nth-child(2) .stButton > button {
            background: linear-gradient(90deg, #0d9488, #2dd4bf) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 12px 0 !important;
            letter-spacing: .5px;
            box-shadow: 0 4px 20px rgba(45,212,191,0.30) !important;
            transition: opacity .2s, transform .15s !important;
          }
          div[data-testid="column"]:nth-child(2) .stButton > button:hover {
            opacity: .88 !important; transform: translateY(-1px);
          }
        </style>
        """, unsafe_allow_html=True)

        pwd = st.text_input(
            "密码", type="password",
            placeholder="请输入访问密码",
            label_visibility="collapsed",
        )
        btn = st.button("进入系统 →", use_container_width=True, type="primary")

    if btn or pwd:
        if pwd == CORRECT_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        elif pwd:
            _, col2, _ = st.columns([1, 1, 1])
            with col2:
                st.error("密码错误，请重试")

# ── 已认证：全屏嵌入 HTML ─────────────────────────────────────
else:
    st.markdown("""
    <style>
      .block-container { padding: 0 !important; max-width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=5000, scrolling=True)
