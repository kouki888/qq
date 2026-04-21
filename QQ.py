import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# =========================
# 🔑 載入 API KEY
# =========================
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ 請設定 GOOGLE_API_KEY")
    st.stop()

genai.configure(api_key=API_KEY)

# =========================
# 🤖 模型自動選擇（防404）
# =========================
def get_model():
    model_names = ["gemini-2.5-flash"]
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            return model
        except:
            continue
    
    st.error("❌ 無可用模型")
    st.stop()

# =========================
# 🧠 Gemini 法律分析
# =========================
def analyze_with_ai(text):
    model = get_model()

    prompt = f"""
你是一位台灣法律專家，請分析以下案件：

【案件內容】
{text}

請分成兩個部分輸出：

========================
【第一部分：基本法律分析】
========================
【可能涉及罪名】
- 

【法律依據】
- 

【構成要件分析】
- 

【可能法律責任】
- 

========================
【第二部分：進階分析】
========================
【檢察官觀點】
-

【辯護律師觀點】
-

【法官觀點】
-

【消費者觀點】
-

【模擬判決結果】
（請用法院判決書格式：主文 / 理由 / 結果）

【風險等級】
（低 / 中 / 高）
"""

    response = model.generate_content(prompt)
    return response.text

# =========================
# 🗂️ 初始化 session
# =========================
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "topic_ids" not in st.session_state:
    st.session_state.topic_ids = []

if "current_topic" not in st.session_state:
    st.session_state.current_topic = "new"

# =========================
# 🎨 UI 主畫面
# =========================
st.set_page_config(page_title="法律AI分析系統", page_icon="⚖️")

st.title("⚖️ 法律情境分析系統（Gemini AI）")
st.write("輸入情境，AI將自動分析涉及的法條與責任")

# =========================
# ✏️ 使用者輸入
# =========================
user_input = st.text_area("📌 請輸入案件情境", height=150)

if st.button("🔍 開始分析"):

    if user_input.strip() == "":
        st.warning("請輸入內容")
    else:
        with st.spinner("AI分析中..."):
            try:
                result = analyze_with_ai(user_input)

                # 存成新對話
                topic_id = len(st.session_state.topic_ids)
                st.session_state.topic_ids.append(topic_id)

                st.session_state.conversations[topic_id] = {
                    "title": user_input[:10],
                    "content": result
                }

                st.session_state.current_topic = topic_id

            except Exception as e:
                st.error(f"❌ 錯誤：{e}")

# =========================
# 📄 顯示結果
# =========================
if st.session_state.current_topic != "new":
    data = st.session_state.conversations[st.session_state.current_topic]

    st.markdown("---")
    st.subheader(f"📂 案件：{data['title']}")

    # ✨ 分割 AI 回答
    content = data["content"]

    tab1, tab2 = st.tabs(["📘 基本法律分析", "⚖️ 多角色 + 模擬判決"])

    with tab1:
        if "第一部分" in content:
            st.markdown("### 📘 基本法律分析")
            st.write(content.split("第二部分")[0])
        else:
            st.write(content)

    with tab2:
        st.markdown("### ⚖️ 多角色分析 + 模擬判決")

        if "第二部分" in content:
            second_part = content.split("第二部分：進階分析")[-1]
            st.write(second_part)
        else:
            st.warning("⚠️ 尚無進階分析內容")

# =========================
# 📚 側邊欄
# =========================
with st.sidebar:
    st.header("🗂️ 案件紀錄")

    if st.button("🆕 新案件"):
        st.session_state.current_topic = "new"

    for tid in st.session_state.topic_ids:
        title = st.session_state.conversations[tid]["title"]

        label = f"✔️ {title}" if tid == st.session_state.current_topic else title

        if st.button(label, key=f"topic_{tid}"):
            st.session_state.current_topic = tid

    st.markdown("---")

    if st.button("🧹 清除紀錄"):
        st.session_state.conversations = {}
        st.session_state.topic_ids = []
        st.session_state.current_topic = "new"
