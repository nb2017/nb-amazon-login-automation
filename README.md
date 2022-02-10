## アマゾンアカウント自動ログイン

### 準備
1. 下記コマンドを実行しログイン用設定ファイルをローカルにコピーする

    ~~~bash
    $ cd settings
    $ cp amazon_login_setting.json.example amazon_login_setting.json
    ~~~

1. ローカルにコピーした設定ファイルを開き、ログイン用メールアドレス、パスワードを設定する

## 実行

下記コマンドで自動ログインのプログラムを実行できる
```bash
$ python3 index.py
```
