import streamlit as st

st.set_page_config(page_title="法律情境分析系統", page_icon="⚖️")

# =========================
# 📚 法律資料庫（可擴充）
# =========================
laws = [
    {
        "name": "詐欺罪",
        "law": "刑法第339條",
        "category": "刑事",
        "keywords": ["騙", "詐騙", "投資", "匯款"],
        "element": "以詐術使人交付財物",
        "penalty": "5年以下有期徒刑、拘役或罰金"
    },
    {
        "name": "竊盜罪",
        "law": "刑法第320條",
        "category": "刑事",
        "keywords": ["偷", "竊"],
        "element": "竊取他人財物",
        "penalty": "5年以下有期徒刑"
    },
    {
        "name": "公然侮辱",
        "law": "刑法第309條",
        "category": "刑事",
        "keywords": ["罵", "羞辱"],
        "element": "公開侮辱他人",
        "penalty": "拘役或罰金"
    },
    {
        "name": "誹謗罪",
        "law": "刑法第310條",
        "category": "刑事",
        "keywords": ["造謠", "抹黑"],
        "element": "散布不實言論",
        "penalty": "2年以下有期徒刑"
    },
    {
        "name": "傷害罪",
        "law": "刑法第277條",
        "category": "刑事",
        "keywords": ["打", "受傷"],
        "element": "對他人身體造成傷害",
        "penalty": "3年以下有期徒刑"
    },
    {
        "name": "加班費",
        "law": "勞動基準法第24條",
        "category": "行政",
        "keywords": ["加班", "沒給錢"],
        "element": "加班應給付加班費",
        "penalty": "罰鍰2萬～100萬元"
    },
    {
        "name": "工時",
        "law": "勞動基準法第30條",
        "category": "行政",
        "keywords": ["超時工作"],
        "element": "每日工時不得超過8小時",
        "penalty": "罰鍰"
    },
    {
        "name": "個資法",
        "law": "個人資料保護法",
        "category": "行政",
        "keywords": ["偷拍", "未經同意拍照"],
        "element": "未經同意蒐集個資",
        "penalty": "罰鍰或刑責"
    },
    {
        "name": "侵權行為",
        "law": "民法",
        "category": "民事",
        "keywords": ["損害", "賠償"],
        "element": "侵害他人權利應負損害賠償",
        "penalty": "民事賠償"
    }
]

# =========================
# 🔍 分析引擎（加權判斷）
# =========================
def analyze_case(text):
    results = []

    for law in laws:
        score = 0

        for keyword in law["keywords"]:
            if keyword in text:
                score += 1

        if score > 0:
            law_copy = law.copy()
            law_copy["score"] = score
            results.append(law_copy)

    # 依關聯度排序
    results.sort(key=lambda x: x["score"], reverse=True)

    return results


# =========================
# 🎨 UI 介面
# =========================
st.title("⚖️ 法律情境分析系統")
st.write("輸入一段情境，系統將自動分析涉及的法條與責任")

text = st.text_area("📌 請輸入情境描述：")

if st.button("🔍 開始分析"):

    if text.strip() == "":
        st.warning("請先輸入情境")
    else:
        results = analyze_case(text)

        if not results:
            st.error("⚠️ 無法判斷相關法條（請嘗試不同描述）")
        else:
            st.success("分析完成！")

            for i, r in enumerate(results, 1):
                st.markdown(f"---")
                st.subheader(f"📚 分析結果 {i}")

                st.write(f"📌 法條名稱：{r['name']}")
                st.write(f"📖 條文依據：{r['law']}")
                st.write(f"📂 類型：{r['category']}")
                st.write(f"🧠 構成要件：{r['element']}")
                st.write(f"⚖️ 處罰：{r['penalty']}")
                st.write(f"📊 關聯程度：{r['score']}")
