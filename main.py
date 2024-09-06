import streamlit as st
import requests
import openai
import json

# ChatGPT APIキーの設定
openai.api_key = "YOUR_OPENAI_API_KEY"

# APIエンドポイントとJPOのAPIキー
JPO_API_URL = "https://ip-data.jpo.go.jp/api/v1/patents"
JPO_API_KEY = "YOUR_JPO_API_KEY"

# キーワード入力のStreamlitフォーム
st.title("JPO API Keyword Search and Initial Review with ChatGPT")
keyword = st.text_input("Enter keyword to search patents")

if keyword:
    # JPO APIリクエストヘッダー
    headers = {
        "Authorization": f"Bearer {JPO_API_KEY}"
    }

    # APIリクエスト
    response = requests.get(f"{JPO_API_URL}?keyword={keyword}", headers=headers)
    
    if response.status_code == 200:
        patents_data = response.json()

        # 取得データの表示
        st.subheader(f"Results for '{keyword}'")
        st.write(patents_data)  # 生データ表示（デバッグ用）

        # 取得データをChatGPTに渡す（RAGプロセス）
        context = json.dumps(patents_data)[:3000]  # 最大トークン数対策
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please summarize the following patent data: {context}"}
            ]
        )
        
        # ChatGPTの要約結果を表示
        chatgpt_summary = response["choices"][0]["message"]["content"]
        st.subheader("Summary")
        st.write(chatgpt_summary)
        
    else:
        st.error("Failed to retrieve data from JPO API.")
