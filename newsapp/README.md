# newsapp

登録した RSS/Atom フィードから記事を自動で集めて、新着順に一覧表示するニュースキュレーションアプリです。

## できること

- フィードの登録・削除（表示名を省略するとフィード側のタイトルを自動で使います）
- 「更新」ボタンで全フィード、または個別フィードから記事を取得
- 取得済みの記事は `guid` で重複判定するので、何度更新しても増えません
- フィードごとの絞り込みと、20件ずつのページング

## 起動方法

```bash
cd newsapp
python -m venv .venv
source .venv/bin/activate        # Windows は .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

http://127.0.0.1:5000/ を開き、ヘッダーの「更新」を押すと記事が集まります。
`instance/database.db` は初回起動時に自動生成されます。

## 構成

| ファイル | 役割 |
| --- | --- |
| `app/__init__.py` | `create_app()`。拡張の初期化と Blueprint の登録 |
| `app/models.py` | `Feed` / `Article` モデル |
| `app/feeds.py` | RSS の取得・パース・重複除外 |
| `app/routes.py` | 記事一覧（`article_bp`）とフィード管理（`feed_bp`） |
| `app/forms.py` | フィード追加フォーム |
| `app/seeds.py` | 初回起動時に入れる既定フィード |

## 設計メモ

- **日時の扱い**: 日時はすべて「naive な JST」で保存しています。feedparser が返す時刻は
  常に UTC なので、`app/feeds.py` の `published_at()` で JST に変換してから `tzinfo` を落として
  います。aware と naive が混ざると比較時に例外になるため、どちらかに統一するのが安全です。
- **`default=` はコールバックで渡す**: `db.Column(..., default=now_jst)` のように関数オブジェクトを
  渡します。`default=now_jst()` と書くとインポート時に一度だけ評価され、全レコードが同じ時刻に
  なってしまいます。
- **重複除外**: `Article` に `(feed_id, guid)` のユニーク制約を張っています。`guid` はフィードの
  エントリ ID、無い場合は記事 URL を使います。
- **削除のカスケード**: `Feed.articles` に `cascade='all, delete-orphan'` を指定しているので、
  フィードを消すとその記事も一緒に消えます。
- **認証は未実装**: ユーザーごとのデータを持たない構成のため省いています。フィード管理を保護したい
  場合は、`todoapp` と同じ Flask-Login を入れて `feed_bp` のビューに `@login_required` を付けるのが
  手軽です。
- **取得は手動トリガー**: 「更新」ボタン起点です。定期実行にしたい場合は cron や APScheduler から
  `app/feeds.py` の `fetch_all()` をアプリケーションコンテキスト内で呼んでください。
