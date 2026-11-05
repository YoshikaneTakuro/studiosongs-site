# -*- coding: utf-8 -*-
"""ページを組み立てるスクリプト（手元で1回動かして public/ を作るためのもの。
Cloudflare Pages ではビルド不要で、public/ をそのまま公開します）

  python3 scripts/build.py

- src/top-body.html … トップページの本文（旧Wixの埋め込みコードから移したもの）
- src/rules/*.txt   … 会員規約・サブスク規約の本文（1行1段落。「■」で始まる行は見出し）
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / 'src', ROOT / 'public'
SITE = 'https://www.studiosongs.net'

LINE_BODY = ('【種別】個人練習 または 部屋貸し\n【日付】2026/11/3\n【時間】18:00〜20:00\n【部屋】B\n【お名前】\n'
             '【会員番号】会員カードのお名前の横の番号(無ければ空欄)\n【電話番号】\n【人数】1')


def head(title, desc, path, extra=''):
    url = SITE + path
    return f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="STUDIO SONGS">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/images/og.jpg"><meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@STUDIOSONGS758">
<meta name="theme-color" content="#c2006b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/images/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Oswald:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">
{extra}</head>
<body>
<a id="top"></a>
'''


def topbar_and_footer():
    body = (SRC / 'top-body.html').read_text(encoding='utf-8')
    tb = re.search(r'<div class="topbar".*?</nav></div>', body, re.S).group(0)
    ft = re.search(r'<div id="s10" class="seg">.*?</footer>\s*</div>', body, re.S).group(0)
    return tb, ft


def build_top():
    body = (SRC / 'top-body.html').read_text(encoding='utf-8')
    ld = (SRC / 'structured-data.json').read_text(encoding='utf-8').strip()
    extra = f'<script type="application/ld+json">{ld}</script>\n'
    page = head('STUDIO SONGS｜名古屋・千種区の音楽スタジオ（バンド練習・レコーディング）',
                '名古屋市千種区の音楽スタジオ STUDIO SONGS（スタジオソングス）。バンド練習・個人練習・レコーディングに対応。'
                '料金・空き状況の確認とオンライン予約、アクセス情報はこちら。TEL 052-760-6607／定休日 水曜。', '/', extra)
    (OUT / 'index.html').write_text(page + body + '\n</body></html>\n', encoding='utf-8')


RULE_CSS = '''<style>
#s01 .rules{max-width:820px;margin:0 auto;padding:44px 20px 64px}
#s01 .rules h1{font-size:clamp(24px,5.4vw,34px);line-height:1.4;margin:6px 0 10px}
#s01 .rules .lead{color:var(--mute);margin:0 0 28px}
#s01 .rules h2{font-size:clamp(19px,4.6vw,23px);line-height:1.5;margin:38px 0 6px;padding-left:12px;border-left:6px solid var(--pink)}
#s01 .rules .sum{display:block;font-size:14px;font-weight:500;color:var(--pink-d);margin:0 0 10px}
#s01 .rules p{margin:0 0 12px}
#s01 .rules .fee{background:var(--soft);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin:6px 0 14px}
#s01 .rules .fee p{margin:4px 0}
#s01 .rules .upd{margin-top:40px;color:var(--mute);text-align:right}
#s01 .rules .back{display:inline-block;margin-top:24px;font-weight:700;color:var(--pink-d)}
</style>
'''


def build_rules(slug, title, desc):
    tb, ft = topbar_and_footer()
    lines = [l.rstrip() for l in (SRC / 'rules' / f'{slug}.txt').read_text(encoding='utf-8').splitlines()]
    h1, lead, rest = lines[0], lines[1], lines[2:]
    out = [f'<p class="eyebrow">RULES</p><h1>{html.escape(h1)}</h1><p class="lead">{html.escape(lead)}</p>']
    in_fee = False
    for l in rest:
        if not l.strip():
            continue
        if l.startswith('■'):
            if in_fee:
                out.append('</div>'); in_fee = False
            t, _, s = l[1:].partition('・・・')
            out.append(f'<h2>{html.escape(t)}</h2>' + (f'<span class="sum">{html.escape(s)}</span>' if s else ''))
        elif l.startswith('＊'):
            if not in_fee:
                out.append('<div class="fee">'); in_fee = True
            out.append(f'<p>{html.escape(l[1:])}</p>')
        elif l.startswith('更新：'):
            if in_fee:
                out.append('</div>'); in_fee = False
            out.append(f'<p class="upd">{html.escape(l[3:])}</p>')
        else:
            if in_fee:
                out.append('</div>'); in_fee = False
            out.append(f'<p>{html.escape(l)}</p>')
    out.append('<a class="back" href="/">← STUDIO SONGS トップへ</a>')
    page = head(f'{title}｜STUDIO SONGS（名古屋市千種区の音楽スタジオ）', desc, f'/{slug}', RULE_CSS)
    page += f'<div id="s01" class="seg">\n{tb}\n<main class="rules">\n' + '\n'.join(out) + '\n</main>\n</div>\n'
    page += ft + '\n</body></html>\n'
    (OUT / f'{slug}.html').write_text(page, encoding='utf-8')


def build_404():
    tb, ft = topbar_and_footer()
    page = head('ページが見つかりません｜STUDIO SONGS', 'お探しのページは見つかりませんでした。', '/404',
                RULE_CSS + '<meta name="robots" content="noindex">\n')
    page += (f'<div id="s01" class="seg">\n{tb}\n<main class="rules"><h1>ページが見つかりません</h1>'
             '<p>お探しのページは移動したか、なくなった可能性があります。</p>'
             '<a class="back" href="/">← STUDIO SONGS トップへ</a></main>\n</div>\n' + ft + '\n</body></html>\n')
    (OUT / '404.html').write_text(page, encoding='utf-8')


if __name__ == '__main__':
    build_top()
    build_rules('membershiprules', '会員規約',
                'STUDIO SONGS（名古屋市千種区の音楽スタジオ）の会員規約。入会金1,100円の永久会員制、予約・キャンセル料、スタジオ利用の注意点。')
    build_rules('subscription', 'サブスク会員規約',
                'STUDIO SONGSのサブスク会員（月額11,000円でスタジオ使い放題）の利用規約。料金、予約・キャンセル、利用の注意点。')
    build_404()
    print('built:', sorted(p.name for p in OUT.glob('*.html')))
