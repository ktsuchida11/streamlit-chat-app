# streamlit-chat-app の使い方

Pyhton３.10を利用する
Amazon Linux２を利用する場合はOpneSSLが古くPython３.10がインストールできないので入れ替える
```sh
yum remove -y openssl openssl-devel 
yum install -y openssl11 openssl11-devel
```

最低限必要なパッケージ
```sh
pip install duckduck-search
pip install wikipedia
pip install langchain
pip install openai
pip install python-dotenv
```

.envファイルを作成する

```sh
touch .env
```

作成したファイルを編集する

```sh
vi .env
```

作成したファイルに以下の情報を追加する

```sh
OPENAI_API_KEY=＜取得したAPI Key＞
OPENAI_API_MODEL=gpt-3.5-turbo
OPENAI_API_TEMPERATURE=0.5
```

実行する
```sh
streamlit run app.py --server.port 8080
```
