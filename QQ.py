import streamlit as st
import google.generativeai as genai

# =========================
# 🎨 基本設定
# =========================
st.set_page_config(page_title="法律AI分析系統", page_icon="⚖️", layout="wide")

st.title("⚖️ 法律AI分析系統（專題完整版）")
st.write("輸入案件情境，由AI進行法律分析、多角色攻防與模擬判決")

# =========================
# 🔑 Sidebar API Key
# =========================
with st.sidebar:
    st.header("🔑 系統設定")

    API_KEY = st.text_input("輸入 Google API Key", type="password")

    if API_KEY:
        genai.configure(api_key=API_KEY)
    else:
        st.warning("⚠️ 請輸入 API Key 才能使用 AI")

    st.markdown("---")

    st.header("🗂️ 功能選單")

    if st.button("🆕 新案件"):
        st.session_state.current_topic = "new"

    if st.button("🧹 清除紀錄"):
        st.session_state.conversations = {}
        st.session_state.topic_ids = []
        st.session_state.current_topic = "new"

# =========================
# 🧠 模型
# =========================
def get_model():
    return genai.GenerativeModel("gemini-3.0-flash")

# =========================
# ⚖️ AI分析核心
# =========================
def analyze_with_ai(text):
    model = get_model()

    prompt = f"""
你是一位台灣法律專家，請分析以下案件：

【案件內容】
{text}

請分成兩大部分：

========================
【第一部分：基本法律分析】
========================
【可能涉及罪名】
【法律依據】
【構成要件分析】
【可能法律責任】

========================
【第二部分：進階分析】
========================
【檢察官觀點】
【辯護律師觀點】
【法官觀點】
【消費者觀點】

【模擬判決結果】
（請用法院判決書格式：主文 / 理由 / 結果）

【風險等級】
（低 / 中 / 高）
"""

    response = model.generate_content(prompt)
    return response.text

# =========================
# 🗂️ session 初始化
# =========================
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "topic_ids" not in st.session_state:
    st.session_state.topic_ids = []

if "current_topic" not in st.session_state:
    st.session_state.current_topic = "new"

# =========================
# ✏️ 輸入區
# =========================
user_input = st.text_area("📌 請輸入案件情境", height=150)

if st.button("🔍 開始分析"):

    if not API_KEY:
        st.error("❌ 請先輸入 API Key")
        st.stop()

    if user_input.strip() == "":
        st.warning("請輸入內容")
    else:
        with st.spinner("AI分析中..."):
            try:
                result = analyze_with_ai(user_input)

                topic_id = len(st.session_state.topic_ids)
                st.session_state.topic_ids.append(topic_id)

                st.session_state.conversations[topic_id] = {
                    "title": user_input[:12],
                    "content": result
                }

                st.session_state.current_topic = topic_id

            except Exception as e:
                st.error(f"❌ 錯誤：{e}")

# =========================
# 📄 顯示結果（Tabs）
# =========================
if st.session_state.current_topic != "new":

    data = st.session_state.conversations[st.session_state.current_topic]
    content = data["content"]

    st.markdown("---")
    st.subheader(f"📂 案件：{data['title']}")

    tab1, tab2 = st.tabs(["📘 基本法律分析", "⚖️ 多角色 + 判決"])

    # =====================
    # 📘 Tab1
    # =====================
    with tab1:
        st.markdown("### 📘 基本法律分析")

        if "第一部分" in content:
            st.write(content.split("第二部分")[0])
        else:
            st.write(content)

    # =====================
    # ⚖️ Tab2
    # =====================
    with tab2:
        st.markdown("### ⚖️ 多角色分析與模擬判決")

        st.write(content)

# =========================
# 📚 側邊歷史紀錄
# =========================
with st.sidebar:
    st.markdown("---")
    st.header("🗂️ 案件紀錄")

    for tid in st.session_state.topic_ids:
        title = st.session_state.conversations[tid]["title"]

        if st.button(f"📄 {title}", key=f"t_{tid}"):
            st.session_state.current_topic = tid
