from pathlib import Path
import zipfile, os

base = Path('/mnt/data/paper-strip-component')
base.mkdir(parents=True, exist_ok=True)

css = r'''/* =========================================================
   PAPER STRIP COMPONENT — 可直接貼進你的網站 CSS
   適用風格：舊紙、撕邊紙條、手貼註解、引言紙條
   會自動沿用你網站現有的 --font-serif / --ink / --line 等變數
   ========================================================= */

:root {
  --paper-strip-bg: #f4f0e8;
  --paper-strip-bg-2: #e8e2d7;
  --paper-strip-ink: rgba(28, 19, 10, 0.74);
  --paper-strip-line: rgba(28, 19, 10, 0.08);
  --paper-strip-shadow: rgba(28, 19, 10, 0.12);
}

.paper-strip {
  --strip-bg: var(--paper-strip-bg);
  --strip-bg-2: var(--paper-strip-bg-2);
  --strip-ink: var(--paper-strip-ink);
  position: relative;
  display: block;
  width: fit-content;
  max-width: min(760px, 100%);
  margin: 22px 0;
  padding: 16px 36px;
  color: var(--strip-ink);
  font-family: var(--font-serif, "Noto Serif TC", "Songti TC", "PMingLiU", serif);
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.85;
  letter-spacing: 0.07em;
  text-align: left;
  background:
    radial-gradient(circle at 13% 28%, rgba(255,255,255,0.42) 0 1px, transparent 2px),
    radial-gradient(circle at 48% 72%, rgba(28,19,10,0.045) 0 1px, transparent 2px),
    radial-gradient(circle at 82% 42%, rgba(255,255,255,0.25) 0 1px, transparent 2px),
    repeating-linear-gradient(8deg, rgba(28,19,10,0.018) 0, rgba(28,19,10,0.018) 1px, transparent 1px, transparent 7px),
    linear-gradient(180deg, var(--strip-bg) 0%, var(--strip-bg-2) 100%);
  border: 1px solid var(--paper-strip-line);
  clip-path: polygon(0.8% 7%, 4% 3%, 9% 5%, 14% 2%, 20% 5%, 27% 3%, 34% 4%, 42% 2%, 49% 5%, 56% 3%, 63% 4%, 70% 2%, 78% 4%, 86% 3%, 94% 5%, 99.2% 3%, 98.8% 93%, 94% 96%, 88% 95%, 80% 98%, 73% 95%, 66% 97%, 59% 95%, 51% 98%, 44% 96%, 36% 97%, 29% 95%, 21% 98%, 14% 95%, 7% 97%, 1.2% 94%);
  filter: drop-shadow(0 7px 11px var(--paper-strip-shadow)) drop-shadow(0 1px 0 rgba(255,255,255,0.42));
  transform: rotate(-0.7deg);
  transform-origin: 50% 50%;
}
.paper-strip > * { position: relative; z-index: 2; }
.paper-strip .paper-strip-text { display: block; }
.paper-strip .paper-strip-text::before { content: ""; position: absolute; inset: -12px -24px; z-index: -1; pointer-events: none; background: radial-gradient(circle at 0% 0%, rgba(28,19,10,0.07), transparent 38%), radial-gradient(circle at 100% 100%, rgba(28,19,10,0.05), transparent 36%); opacity: 0.42; }
.paper-strip--sm { padding: 10px 24px; font-size: 0.88rem; line-height: 1.75; letter-spacing: 0.06em; }
.paper-strip--lg { padding: 22px 44px; font-size: clamp(1.04rem, 1.55vw, 1.18rem); line-height: 1.9; }
.paper-strip--wide { width: min(760px, 100%); }
.paper-strip--narrow { max-width: min(520px, 100%); }
.paper-strip--left { margin-left: 0; margin-right: auto; text-align: left; }
.paper-strip--center { margin-left: auto; margin-right: auto; text-align: center; }
.paper-strip--right { margin-left: auto; margin-right: 0; text-align: left; }
.paper-strip--tilt-1 { transform: rotate(-1.4deg); }
.paper-strip--tilt-2 { transform: rotate(0.8deg); }
.paper-strip--tilt-3 { transform: rotate(-0.4deg); }
.paper-strip--tilt-4 { transform: rotate(1.2deg); }
.paper-strip--warm { --strip-bg: #f5efe4; --strip-bg-2: #e9dfd1; }
.paper-strip--pink { --strip-bg: #f5e8ec; --strip-bg-2: #ead8df; }
.paper-strip--pale-gold { --strip-bg: #f1ead8; --strip-bg-2: #e4d6bb; }
.paper-strip--taped { overflow: visible; }
.paper-strip--taped::before, .paper-strip--taped::after { content: ""; position: absolute; top: -8px; z-index: 4; width: 56px; height: 18px; background: repeating-linear-gradient(-8deg, rgba(255,255,255,0.22) 0, rgba(255,255,255,0.22) 2px, transparent 2px, transparent 6px), rgba(204, 185, 139, 0.38); border: 1px solid rgba(28, 19, 10, 0.05); box-shadow: 0 1px 2px rgba(28, 19, 10, 0.08); backdrop-filter: blur(1px); clip-path: polygon(2% 12%, 10% 0, 22% 8%, 34% 0, 48% 8%, 60% 0, 74% 8%, 86% 0, 98% 10%, 100% 90%, 88% 100%, 76% 92%, 62% 100%, 50% 92%, 38% 100%, 25% 92%, 12% 100%, 0 88%); }
.paper-strip--taped::before { left: 28px; transform: rotate(-5deg); }
.paper-strip--taped::after { right: 28px; transform: rotate(6deg); }
.paper-strip-title { color: rgba(122, 37, 32, 0.82); font-size: clamp(1rem, 1.8vw, 1.25rem); font-weight: 700; letter-spacing: 0.1em; }
.paper-strip-quote { color: rgba(28, 19, 10, 0.78); font-size: clamp(1.05rem, 1.7vw, 1.25rem); }
.paper-strip-quote .quote-mark { color: rgba(122, 37, 32, 0.7); font-size: 1.12em; }
.paper-strip-hint { color: rgba(28, 19, 10, 0.62); font-size: 0.88rem; }
.paper-strip-hint strong { color: rgba(122, 37, 32, 0.78); font-weight: 700; }
.paper-strip.is-clickable { cursor: pointer; transition: transform 0.22s ease, filter 0.22s ease; }
.paper-strip.is-clickable:hover { transform: rotate(-0.2deg) translateY(-2px); filter: drop-shadow(0 10px 14px rgba(28, 19, 10, 0.15)) drop-shadow(0 1px 0 rgba(255,255,255,0.42)); }
@media (max-width: 640px) { .paper-strip { max-width: calc(100vw - 36px); padding: 13px 24px; font-size: 0.92rem; line-height: 1.75; letter-spacing: 0.055em; } .paper-strip--lg { padding: 18px 28px; font-size: 1rem; } .paper-strip--taped::before, .paper-strip--taped::after { width: 44px; height: 15px; top: -7px; } .paper-strip--taped::before { left: 22px; } .paper-strip--taped::after { right: 22px; } }
@media (prefers-reduced-motion: reduce) { .paper-strip.is-clickable { transition: none; } .paper-strip.is-clickable:hover { transform: none; } }
'''

snippet = r'''<!-- ======================================================
     紙條元件 HTML 範例
     把這些片段放進你想出現紙條的位置
     ====================================================== -->

<!-- 1. 小標紙條 -->
<div class="paper-strip paper-strip--center paper-strip--wide paper-strip-title paper-strip--tilt-1">
  <span class="paper-strip-text">那些被聲音接住的時刻</span>
</div>

<!-- 2. 引言紙條 -->
<div class="paper-strip paper-strip--lg paper-strip--center paper-strip--taped paper-strip-quote paper-strip--tilt-2">
  <span class="paper-strip-text">
    <span class="quote-mark">「</span>有時候我不是想聽內容，我只是想知道，有人在說話。<span class="quote-mark">」</span>
  </span>
</div>

<!-- 3. 互動提示紙條 -->
<div class="paper-strip paper-strip--sm paper-strip--right paper-strip-hint paper-strip--pink paper-strip--tilt-4 is-clickable">
  <span class="paper-strip-text"><strong>小提醒：</strong>點擊卡片可展開更多觀點。</span>
</div>

<!-- 4. 專家段落前的小紙條 -->
<div class="paper-strip paper-strip--narrow paper-strip--left paper-strip--pale-gold paper-strip--tilt-3">
  <span class="paper-strip-text">心理師怎麼看？聲音陪伴為什麼會帶來熟悉感？</span>
</div>
'''

html = '<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>紙條元件預覽</title><link rel="stylesheet" href="paper-strip.css"></head><body style="background:#f9e6ec;font-family:serif;padding:80px"><h1>紙條元件預覽</h1>' + snippet + '</body></html>'

readme = '''# 紙條元件 paper-strip-component

這份資料夾包含：

1. `paper-strip.css`：完整紙條元件 CSS，可直接貼到網站主 CSS 最後面。
2. `paper-strip-snippets.html`：可直接貼進網頁 HTML 的範例片段。
3. `index.html`：紙條預覽頁。

## 整合方式

把 `paper-strip.css` 的內容貼到主 CSS 最底部，再到 `paper-strip-snippets.html` 複製需要的紙條片段，貼到文章段落、互動區塊或專家卡片附近。
'''

(base / 'paper-strip.css').write_text(css, encoding='utf-8')
(base / 'index.html').write_text(html, encoding='utf-8')
(base / 'paper-strip-snippets.html').write_text(snippet, encoding='utf-8')
(base / 'README.md').write_text(readme, encoding='utf-8')

zip_path = Path('/mnt/data/paper-strip-component.zip')
if zip_path.exists():
    zip_path.unlink()
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in base.rglob('*'):
        z.write(p, p.relative_to(base.parent))
print(zip_path.as_posix())
