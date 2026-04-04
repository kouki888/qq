import streamlit as st

st.set_page_config(page_title="法律情境分析系統", page_icon="⚖️")

st.title("⚖️ 法律情境分析系統")
st.write("輸入一段情境，系統將分析涉及的法條與責任")

# 使用者輸入
text = st.text_area("請輸入情境描述：")

def analyze_case(text):
    results = []

    # 詐欺罪
    if any(k in text for k in ["騙", "詐騙", "投資", "匯款"]):
        results.append({
            "law": "刑法第339條（詐欺罪）",
            "element": "以詐術使人交付財物",
            "penalty": "5年以下有期徒刑、拘役或罰金"
        })

    # 竊盜罪
    if any(k in text for k in ["偷", "竊"]):
        results.append({
            "law": "刑法第320條（竊盜罪）",
            "element": "竊取他人財物",
            "penalty": "5年以下有期徒刑"
        })

    # 公然侮辱
    if any(k in text for k in ["罵", "羞辱"]):
        results.append({
            "law": "刑法第309條（公然侮辱）",
            "element": "公開侮辱他人",
            "penalty": "拘役或罰金"
        })

    # 誹謗罪
    if any(k in text for k in ["造謠", "抹黑"]):
        results.append({
            "law": "刑法第310條（誹謗罪）",
            "element": "散布不實言論",
            "penalty": "2年以下有期徒刑"
        })

    # 勞基法
    if "加班" in text and "沒給錢" in text:
        results.append({
            "law": "勞動基準法第24條",
            "element": "加班應給付加班費",
            "penalty": "可處罰鍰（2萬～100萬）"
        })

    # 偷拍 / 個資
    if any(k in text for k in ["偷拍", "未經同意拍照"]):
        results.append({
            "law": "個人資料保護法",
            "element": "未經同意蒐集個資",
            "penalty": "罰鍰或刑責"
        })

    return results


# 按鈕
if st.button("🔍 分析"):
    if text.strip() == "":
        st.warning("請先輸入情境")
    else:
        results = analyze_case(text)

        if not results:
            st.error("⚠️ 無法判斷相關法條")
        else:
            st.success("分析完成！")

            for i, r in enumerate(results, 1):
                st.subheader(f"案例 {i}")
                st.write(f"📌 法條：{r['law']}")
                st.write(f"📖 構成要件：{r['element']}")
                st.write(f"⚖️ 處罰：{r['penalty']}")
