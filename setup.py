# setup.py

# 起動コマンド
# >> master\scripts\activate
# (master) >> python setup.py

# 環境構築手順
# python 3.12をインストール(pathを通す)
# プロジェクト用のディレクトリ作成＆CDで移動、以下のコマンドで仮想環境を作成
# >> python -m venv master
# 以下コマンドで仮想環境を有効
# >> master\scripts\activate
# 以下コマンドで仮想環境に各種パッケージをインストール
# >> pip install -r requirements.txt(一括インストール)
# >> pip install flask 3.0.0
# >> pip install flask-sqlalchemy 3.1.1
# >> pip install flask-migrate 4.0.5
# >> pip install flask-login 0.6.3
# >> pip install flask-bcrypt 1.0.1
# >> pip install flask-wtf 1.2.1
# >> pip install wtforms 3.1.1
# >> pip install email-validator 2.1.0
# >> pip install PyMySQL 1.1.0

from flaskr.__init__ import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)