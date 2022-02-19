# google-drive-document-ocr
グーグルドライブから画像をドキュメントで開くとOCR結果が出るのを利用してPythonAPIで画像のOCRを行う

<img src="https://user-images.githubusercontent.com/64346215/154796178-84ecab8a-bdfc-4625-becc-b1a81c73d0f9.jpg" width="600px">

## グーグル側の設定
1. googleアカウントにログイン
2. google developer consoleにアクセス
3. Google APIs ダッシュボードからプロジェクト作成
4. APIライブラリから「GoogleDriveAPI」を有効にする
5. 認証情報の作成（OauthクライアントID）
6. 同意画面の設定
7. スコープの設定（GoogleDrive API　../auth/drive）
8. 改めて認証情報の作成
9. 鍵を作成（client_secret.jsonとして保存）

※この記事が詳しく書いてあります。<br>
「https://zenn.dev/wtkn25/articles/python-googledriveapi-auth」
<br>

## クライアント側の設定
1. モジュールをインストール<br>
　ガイドの通り　https://developers.google.com/drive/api/v3/quickstart/python<br>
　$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client
2. リポジトリをクローン
3. 認証情報作成で艇に入れた鍵（client_secret.json）を.pyファイルと同じ階層に移動
4. フォルダIDの設定
5. 実行<br>
   $ python3 drive_api_py.py
