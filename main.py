import streamlit as st
import requests
import openai==0.27.0 
import json

# ChatGPT APIキーの設定
openai.api_key = "YOUR_OPENAI_API_KEY"
import streamlit as st
import openai

# Initialize OpenAI with your API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

st.title("飲みすぎアラート")

# Sidebar for age, gender, and alcohol tolerance
age = st.sidebar.number_input("年齢", min_value=18, max_value=100)
gender = st.sidebar.selectbox("性別", ["男性", "女性", "その他"])
tolerance = st.sidebar.radio("お酒強い・弱い（自覚）", ("強い", "普通", "弱い"))

# Initialize session state to store drinks
if 'drinks' not in st.session_state:
    st.session_state.drinks = []

# Buttons for drink selection
if st.button("ビール大"):
    st.session_state.drinks.append("ビール大")
if st.button("ビール中"):
    st.session_state.drinks.append("ビール中")
if st.button("日本酒"):
    st.session_state.drinks.append("日本酒")
if st.button("ワイン"):
    st.session_state.drinks.append("ワイン")

# Display the consumed drinks
st.subheader("飲んだ内容:")
st.write(", ".join(st.session_state.drinks))

# Function to get advice using OpenAI LLM
def get_drinking_advice(drinks, age, gender, tolerance):
    # Create a prompt for OpenAI
    prompt = f"私は{age}歳の{gender}です。自分はお酒が{tolerance}です。今日飲んだのは、{', '.join(drinks)}です。飲みすぎかどうか、いつもより多いか、明日の気分について教えてください。"

    # Call OpenAI to get the advice
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Generate advice based on the drinks
if st.session_state.drinks:
    advice = get_drinking_advice(st.session_state.drinks, age, gender, tolerance)
    st.subheader("アドバイス:")
    st.write(advice)
