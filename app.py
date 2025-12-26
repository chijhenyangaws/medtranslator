import streamlit as st
from google import genai

# 1. 頁面設定
st.set_page_config(page_title="AI 醫學翻譯官", page_icon="🩺")
st.title("🩺 專業 AI 中翻英工具")
st.caption("基於 Gemini 2.5 Flash 模型製作")

# 2. 從 Streamlit 的 Secrets 讀取 API Key (部署時設定)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("請在 Secrets 中設定 GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)

# 3. 側邊欄：設定翻譯風格
style = st.sidebar.selectbox(
    "選擇翻譯風格",
    ["通用地道", "醫學論文", "臨床病歷", "口語對話"]
)

# 4. 主介面
text_input = st.text_area("請輸入中文內容：", height=200)

if st.button("立即翻譯", type="primary"):
    if text_input:
        with st.spinner("翻譯中..."):
            # 根據選擇調整 Prompt
            prompts = {
                "通用地道": "自然地道的英文。",
                "醫學論文": "學術化、符合 NEJM/Lancet 風格的專業醫學英文。",
                "臨床病歷": "簡潔、使用標準醫學縮寫（如 s/p, c/o, r/o）的臨床風格。",
                "口語對話": "日常、口語化的英文。"
            }
            
            system_prompt = f"你是一位專業翻譯官。請將以下中文翻譯成{prompts[style]}。只回傳結果。"
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=text_input,
                config=genai.types.GenerateContentConfig(system_instruction=system_prompt)
            )
            
            st.subheader("翻譯結果：")
            st.success(response.text)
            st.button("複製結果") # 提示：這只是顯示，進階可加上複製功能
    else:
        st.warning("請先輸入文字")
