import streamlit as st
import os
import json

st.set_page_config(page_title="Debug Mode", layout="wide")

st.title("🕵️‍♂️ 系統診斷模式")
st.markdown("如果這頁能顯示，代表 Streamlit 伺服器運作正常。")

# 1. 檢查當前工作目錄
current_dir = os.getcwd()
st.write(f"📂 目前工作目錄: `{current_dir}`")

# 2. 列出目錄下所有檔案 (這能幫我們確認 my_prompts.json 到底有沒有被上傳成功)
files = os.listdir(".")
st.subheader("📄 伺服器上的檔案列表:")
st.code(files)

# 3. 檢查資料庫檔案
target_file = "my_prompts.json"
if target_file in files:
    st.success(f"✅ 找到檔案: {target_file}")
    
    # 嘗試讀取內容
    try:
        with open(target_file, "r", encoding="utf-8") as f:
            content = json.load(f)
            st.success("✅ JSON 讀取成功！格式正確。")
            
            # 檢查資料結構
            if "roles" in content:
                st.info(f"結構檢查: 發現 'roles' 鍵值，包含 {len(content['roles'])} 個分類。")
            else:
                st.info(f"結構檢查: 直接字典結構，包含 {len(content)} 個分類。")
                
    except json.JSONDecodeError as e:
        st.error(f"❌ JSON 格式嚴重錯誤: {e}")
        st.error("這代表雖然檔案存在，但內容是壞的（可能是亂碼或被截斷）。")
    except Exception as e:
        st.error(f"❌ 其他讀取錯誤: {e}")
else:
    st.error(f"❌ 嚴重警告：找不到 `{target_file}`！")
    st.warning("請檢查：1. GitHub 上真的有這個檔案嗎？ 2. 檔名大小寫完全一樣嗎？")