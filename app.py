import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

# 既存のimportの後に追加
if st.sidebar.button("環境変数の確認"):
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        st.sidebar.success("APIキーが設定されています")
        # セキュリティのため、最初の数文字のみ表示
        st.sidebar.write(f"APIキー: {api_key[:8]}...")
    else:
        st.sidebar.error("APIキーが設定されていません")


from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# LLMを使った簡単なWebアプリ
# ユーザーの入力に応じて専門家の回答を生成する
def get_response(user_input):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    # 選択した専門家に応じてシステムメッセージを設定
    if st.session_state.get('expert') == "食事・栄養の専門家":
        system_message = "あなたは食事と栄養の専門家です。質問内容に専門用語を使わず簡潔に回答してください。"
    elif st.session_state.get('expert') == "睡眠の専門家":
        system_message = "あなたは睡眠の専門家です。質問内容に専門用語を使わず簡潔に回答してください。"
    else:
        system_message = "あなたは一般的なアシスタントです。"   

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_input)
    ]
    result = llm(messages)
    return result.content

# inputでllmを使うサンプル
st.title("サンプルアプリ①: LLMを使った簡単なWebアプリ")
st.write("このアプリは、LLMを使って簡単な会話を行います。")

# ラジオボタンで専門家を選択
expert = st.radio(
    "専門家を選択してください：",
    ("食事・栄養の専門家", "睡眠の専門家")
)

# 選択された専門家に応じてシステムメッセージを設定
if expert == "食事・栄養の専門家":
    system_message = "あなたは食事と栄養の専門家です。"
elif expert == "睡眠の専門家":
    system_message = "あなたは睡眠の専門家です。"

# ユーザー入力用のテキストボックスを作成
user_input = st.text_input("メッセージを入力してください：", key="user_input")

# 送信ボタンが押されたときの処理
if st.button("送信"):
    if user_input:
        response = get_response(user_input)
        st.write("回答：", response)
    else:
        st.warning("メッセージを入力してください。")
