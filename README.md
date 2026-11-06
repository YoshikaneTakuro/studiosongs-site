# STUDIO SONGS 公式サイト（studiosongs.net）

Wix をやめて、**月額0円**で動くスタジオのホームページです。ヨシカネタクロウ公式サイトと同じく Cloudflare Pages（無料）で公開します。

- **ページ**：トップ（料金・スタジオ紹介・サブスク・レコーディング・予約・空き状況・アクセス）、`/subscription`（サブスク会員規約）、`/membershiprules`（会員規約）
- **見た目**：今のWixのトップ（ピンク系の埋め込みコード）をそのまま移しています。Wixの枠に合わせるための縮小・スクロール処理は外したので、スマホで二重スクロールになりません
- **空き状況**：今までどおり予約スプレッドシートの Apps Script（…/exec）から読み込み（個人名は出ません）
- **LINE・メール・電話予約**：今までどおり（テンプレート付きリンク）
- **費用**：ドメイン代のみ（お名前.com）

```
public/          … 公開されるファイル一式（Cloudflare Pages はこのフォルダをそのまま公開）
src/top-body.html … トップページの本文（文章や料金を直すときはここ）
src/rules/*.txt   … 規約の本文（1行1段落、「■」で始まる行が見出し、「＊」はキャンセル料の囲み）
scripts/build.py  … src から public/*.html を作り直す（python3 scripts/build.py）
scripts/wix-images.txt … 旧Wixの画像を取り込むリスト（GitHub が自動で public/images に保存）
```

---

## 公開までの手順（この順番で）

### 1. GitHub（済・Cloudflareと自動連携済み）
リポジトリ `YoshikaneTakuro/studiosongs-site`（Private）に置いてあります。
最初に GitHub の「Actions」で **旧サイト（Wix）の画像を取り込む** が自動で動き、写真・ロゴ・LINEのQRが `public/images` に入ります（Actions タブで緑のチェックになっていればOK）。

### 2. Cloudflare Pages で公開（約5分）
1. https://dash.cloudflare.com →「Workers & Pages → 作成 → Pages → Git に接続」→ `studiosongs-site` を選ぶ
2. ビルド設定
   - フレームワーク：**なし**
   - ビルドコマンド：**空欄**
   - ビルド出力ディレクトリ：`public`
3. 「保存してデプロイ」→ `https://studiosongs-site.pages.dev` で表示を確認
   - 空き状況・LINE予約・メール予約・電話ボタン・地図・時刻表のリンクを、スマホで一通り押してみる

### 3. ドメイン（お名前.com）を新サイトに向ける
1. Cloudflare の studiosongs-site →「設定 → ドメインとルート → 追加 → カスタムドメイン」で **`www.studiosongs.net`** を追加
2. Cloudflare が表示する設定（`www` の **CNAME → studiosongs-site.pages.dev**）を、お名前.com の「DNS設定」で入れる
   - 今 Wix 向けに入っている `www` の CNAME（`…wixdns.net` など）は、この値に**書き換え**ます
   - お名前.com のネームサーバーが Wix のもの（`ns…wixdns.net`）になっている場合は、先にお名前.com の初期ネームサーバーに戻してから設定します
   - **メール（MX）の設定には触りません**
3. `studiosongs.net`（wwwなし）で来た人を www に転送する：お名前.com の「URL転送」で `studiosongs.net → https://www.studiosongs.net`（またはヨシカネサイトと同じ方法）
4. 数十分〜数時間で `https://www.studiosongs.net` が新サイトに切り替わります（鍵マークが付けば完了）

### 4. 検索エンジンに知らせる
1. Google Search Console に `https://www.studiosongs.net` を登録（済みならそのまま）→ サイトマップに `/sitemap.xml` を送信
2. Googleビジネスプロフィールのウェブサイト欄が `https://www.studiosongs.net` になっているか確認

### 5. **最後に** Wix を解約
新サイトがドメインで表示され、空き状況・予約ボタンが動くのを確認してから、Wix の有料プラン（Wix Studio）を解約します。
- 先に解約すると、旧サイトが広告付きの無料URLに戻ります
- ドメインはお名前.com 管理なので、Wix側でドメインの移管は不要です
- 解約後も、念のため Wix のサイト自体（エディタ）はすぐに削除せず残しておくと安心です

---

## ふだんの直し方
| やりたいこと | やり方 |
|---|---|
| 料金・文章を変える | `src/top-body.html` の該当箇所を直す → `python3 scripts/build.py` → GitHub に上げる（Claude に頼めばまとめてやります） |
| 規約を変える | `src/rules/membershiprules.txt` または `subscription.txt` を直す（最後の「更新：」の行も） |
| 写真を差し替える | `public/images/` の同じ名前のファイルを入れ替える（studio-a.jpg など） |
| 空き状況のAPIを変えた | `src/top-body.html` の `var API = '…/exec'` を新しいURLに |

GitHub に上げると、Cloudflare Pages が1分ほどで自動的に反映します。

## 旧サイトのURL
`/`、`/subscription`、`/membershiprules` は同じURLのままです。`/home` などは `public/_redirects` でトップへ転送しています。
