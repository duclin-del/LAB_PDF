import streamlit as st
import json
import os

# --- ⚙️ 設定 ---
LOCAL_DB_FILENAME = "my_prompts.json"

# --- 🎨 頁面設定 ---
st.set_page_config(page_title="Prompt Copilot", page_icon="✈️", layout="wide")

# --- 📦 讀取資料庫函數 ---
@st.cache_data # 這行會讓資料快取，不用每次重新讀取
def load_data():
    if not os.path.exists(LOCAL_DB_FILENAME):
        return None
    with open(LOCAL_DB_FILENAME, 'r', encoding='utf-8') as f:
        return json.load(f)

# --- 🖥️ 主程式 ---
def main():
    # 標題區
    st.title("✈️ AI Prompt Copilot")
    st.markdown("##### 🚀 你的離線版 AI 詠唱助手 (Streamlit 版)")
    
    # 檢查資料庫
    db = load_data()
    if db is None:
        st.error(f"❌ 找不到資料庫檔案 `{LOCAL_DB_FILENAME}`。請確認檔案在同一個資料夾中。")
        return

    # 處理資料結構 (脫殼)
    roles_data = db.get("roles", db)

    # --- 側邊欄：設定區 ---
    with st.sidebar:
        st.header("⚙️ 設定 (Config)")
        
        # 1. 選擇角色
        role_list = list(roles_data.keys())
        selected_role = st.selectbox("📂 角色分類 (Category)", role_list)
        
        # 2. 選擇任務
        task_list = list(roles_data[selected_role].keys()) if selected_role else []
        selected_task = st.selectbox("⚡ 具體任務 (Task)", task_list)
        
        # 3. 輸出模式
        st.markdown("---")
        mode_options = {
            "🚀 智能預設 (Auto)": "",
            "🤫 靜默接收 (Silent Ack)": "【系統提示】：請接收以下輸入內容，但【先不要執行】任何任務。簡單回覆『🆗 收到』即可。\n\n----------------\n\n",
            "📝 純文字模式 (Text Only)": "【系統提示】：輸出結果必須嚴格限制為「純文字」。禁止生成圖片或程式碼。\n\n----------------\n\n",
            "🐍 純代碼模式 (Code Only)": "【系統提示】：針對用戶的問題，【只輸出程式碼區塊】。不要有任何解釋。\n\n----------------\n\n",
            "🌍 翻譯成繁中 (Translate)": "【系統提示】：請將以下內容翻譯成自然、通順的「台灣繁體中文」。\n\n----------------\n\n"
        }
        selected_mode_label = st.selectbox("🎛️ 輸出模式", list(mode_options.keys()))
        selected_mode_prefix = mode_options[selected_mode_label]

    # --- 主畫面：參數輸入區 ---
    if selected_role and selected_task:
        task_data = roles_data[selected_role][selected_task]
        
        # 顯示說明
        if "description" in task_data:
            st.info(f"ℹ️ {task_data['description']}")
            
        st.subheader("🛠️ 參數設定 (Variables)")
        
        # 動態產生輸入框
        user_inputs = {}
        vars_config = task_data.get("vars", {})
        
        # 使用 Columns 排版讓畫面更緊湊
        cols = st.columns(2) 
        idx = 0
        
        for var_name, default_val in vars_config.items():
            col = cols[idx % 2] # 左右交替
            
            if var_name.endswith("__multi") and isinstance(default_val, list):
                clean_name = var_name.replace("__multi", "")
                user_inputs[var_name] = col.multiselect(clean_name, default_val, default=[default_val[0]])
            elif isinstance(default_val, list):
                user_inputs[var_name] = col.selectbox(var_name, default_val)
            else:
                user_inputs[var_name] = col.text_input(var_name, value=str(default_val))
            
            idx += 1

        # --- 生成結果區 ---
        st.markdown("---")
        st.subheader("📝 生成結果 (Result)")

        # 組合 Prompt
        try:
            template = task_data['template']
            # 處理變數 (如果是多選列表，轉成字串)
            format_inputs = {}
            for k, v in user_inputs.items():
                if isinstance(v, list) and k.endswith("__multi"):
                    format_inputs[k] = "、".join(v)
                else:
                    format_inputs[k] = v
            
            final_prompt = selected_mode_prefix + template.format(**format_inputs)
            
            # 顯示結果 (使用 st.code 會有內建複製按鈕)
            st.code(final_prompt, language="markdown")
            
            # 或者用純文字框讓用戶好編輯
            # st.text_area("可編輯區域", final_prompt, height=300)
            
        except Exception as e:
            st.error(f"生成失敗，請檢查模板格式: {e}")

if __name__ == "__main__":
    main()