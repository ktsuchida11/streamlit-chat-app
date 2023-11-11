import os

import streamlit as st

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder


# env ファイルの読み込み
load_dotenv()

# Agentのチェーンを作成する
def create_agent_chain():
    # OpenAI API のチャットモデルをストリーミングで利用するための設定
    chat = ChatOpenAI(
        model_name=os.environ["OPENAI_API_MODEL"],
        temperature=os.environ["OPENAI_API_TEMPERATURE"],
        streaming = True,
    )

    # OpenAI Function AgentのプロンプトにMemoryの会話履歴を追加するための設定
    agent_kwargs = {
        "extra_prompt_messages":[MessagesPlaceholder(variable_name="memory")],
    }
    # OpenAI Function Agentが使える設定でMemoryを初期化
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

    # Web検索もしくは、Wikipediaに情報を検索しにいく
    tools = load_tools(["ddg-search","wikipedia"])
    return initialize_agent(
                tools, 
                chat, 
                agent=AgentType.OPENAI_FUNCTIONS,
                agent_kwargs=agent_kwargs,
                memory=memory)


# main start
# タイトル表示
st.title("streamlit-chat-app")

# セッションにAgentがない場合にChain Agentを作成
if "agent_chain" not in st.session_state:
    st.session_state.agent_chain = create_agent_chain()

# セッションに会話履歴がない場合は初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# ロールに設定されている会話を表示(会話の回答)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 入力欄の初期化
prompt = st.chat_input("what is up?")

# 入力があったら以下の処理を実施する
if prompt:
    # 入力内容を会話履歴に保存
    st.session_state.messages.append({"role":"user","content":prompt})     
    
    # 入力内容を画面に表示
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 入力内容を問い合わせる処理
    with st.chat_message("assistant"):
        # 回答をストリーミングで受け取るCallbackを宣言
        callback = StreamlitCallbackHandler(st.container())
        response = st.session_state.agent_chain.run(prompt, callbacks=[callback])
        st.markdown(response)

    st.session_state.messages.append({"role":"assistant","content":response})
