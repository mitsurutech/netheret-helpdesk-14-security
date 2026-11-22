# Netheretヘルプデスク ステップ14：セキュリティと法律

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

授業のための作例です。16のステップで、小さな会社のITを支える架空の会社Netheretのために、ヘルプデスクのWebアプリを作っていきます。 このステップでは、クロスサイトリクエストフォージェリ（CSRF）への対策、より安全なクッキーとセキュリティヘッダー、UK GDPRのためのプライバシー通知を加えます。

## このステップで加わるもの

- `helpdesk/security.py`：
  - 手で書いたCSRFトークン：セッションに保存したランダムな値を、POSTする
    すべてのフォームの隠しフィールドに入れます。`check_csrf` がリクエストのたびに先に実行され、
    正しいトークンのないPOSTには「400 Bad Request」を返します。
  - すべてのレスポンスにセキュリティヘッダー：自分たちのスクリプトとスタイルだけを
    許可するContent Security Policy、フレームへの埋め込みの禁止、型の推測の禁止。
- セッションクッキーは `HttpOnly` と `SameSite=Lax` で、HTTPSのサーバーで
  `SESSION_COOKIE_SECURE=1` を設定すると `Secure` にもなります。
- `/privacy`：やさしい言葉で書いたプライバシー通知。すべてのページからリンクしています。
- 「400 Bad Request」の、やさしい言葉のページ。

## ここまでのセキュリティを一覧で

| リスク | アプリがしていること | 場所 |
|------|-------------------|-------|
| パスワードの盗難 | ソルト付きのハッシュだけを保存 | `models.py`（`set_password`） |
| 誰がアカウントを持っているかの推測 | サインインの失敗には、どんな場合も同じメッセージ | `auth.py` |
| セッション固定 | サインイン時に `session.clear()` | `auth.py` |
| セッションクッキーの改ざん | 環境変数から読んだ秘密鍵で署名 | `__init__.py` |
| ほかの会社のデータを見る | 顧客のクエリはすべてその会社に限定 | `customer.py`、`tickets.py` |
| 自分の役割でしてはいけないことをする | `@role_required` と、各操作でのチェック | `auth.py`、`jobs.py`、`tickets.py` |
| クロスサイトスクリプティング（XSS） | Jinjaがすべてをエスケープ、`|safe` は使わない、CSP | テンプレート、`security.py` |
| SQLインジェクション | パラメーター付きのSQLAlchemyクエリ、文字列の組み立てはしない | すべての場所 |
| クロスサイトリクエストフォージェリ | POSTするすべてのフォームに手書きのCSRFトークン | `security.py` |
| クリックジャッキング | `X-Frame-Options` と `frame-ancestors` | `security.py` |

関わる法律：UK GDPRとData Protection Act 2018（個人データ、
プライバシー通知、必要なものだけを持つこと）、Computer Misuse Act 1990
（アクセス制御が大切な理由）、Equality Act 2010（アクセシビリティが
おまけではない理由）。

## 動かしてみる

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

どのデモ用アカウントでもサインインします（デモ用パスワード `password123`）。どれかのフォームの
ページのソースを表示すると、隠しフィールド `csrf_token` が見えます。チェックが働くところを見るには、
ブラウザの開発者ツールを開き、フォームから隠しフィールドを削除して
送信します。「That did not work」のページが表示されます。

## 注目するところ

- `secrets.token_hex` がトークンを作ります。`secrets` モジュールは、`random` と違って、
  推測しにくくなければならない値のためのものです。
- `secrets.compare_digest` はトークンを安全に比べます。
- `app.before_request` と `app.after_request` は、各ページを変えずに、
  すべてのリクエストの前後でコードを実行します。

## このステップを学ぶ

これは **Task 2. Developing the solution** の16ステップ中のステップ14です。T Level Digital Software Developmentの無料レッスン（英語）のシリーズで、PythonとFlaskを使い、アジャイルのスプリントでNetheretのヘルプデスクを作ります。このステップのレッスンはこちらです：
[セキュリティと法律](https://mitsurutech.co.uk/resources/t-level/dsd-t2-14-security)。

- 前のステップ：[ステップ13「アクセシビリティの設定」](https://github.com/mitsurutech/netheret-helpdesk-13-accessibility)
- 次のステップ：[ステップ15「手作業のテストとテストログ」](https://github.com/mitsurutech/netheret-helpdesk-15-test-log)
- [T Level Digitalの無料レッスン一覧](https://mitsurutech.co.uk/resources/t-level)
- [これらのレッスンをMitsuruTechでクラスに教える](https://mitsurutech.co.uk/ja/learning)、[料金を見る](https://mitsurutech.co.uk/ja/pricing)、
  [学校で無料の1年を始める](https://mitsurutech.co.uk/ja/signup)

## この作例について

T Level Digital Software Developmentの授業のための作例として、[Mitsuru Technologies](https://mitsurutech.co.uk/ja)（MitsuruTech）が書きました。
Netheret IT Support Solutionsの課題文はPearsonのサンプル評価資料によるものです。このコードと解説は私たち自身のもので、
PearsonやDepartment for Educationが公開、推奨、承認したものではありません。
「T Level」はDepartment for Educationの登録商標です。
