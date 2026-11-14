/* GrowwBizz: justified, hyphenated paragraphs. Also on phones (hyphenation keeps gaps small). Skips centred/right text, headings, buttons, tables, labels. */
(function () {
  var d = document, s = d.createElement('style');
  s.textContent = '.gbj{text-align:justify;text-justify:inter-word;hyphens:auto;-webkit-hyphens:auto;overflow-wrap:break-word}.gbj .gbk{font-weight:700}';
  d.head.appendChild(s);
  if (!d.documentElement.lang) d.documentElement.lang = 'en';
  var SKIP = '.meta,.src,.fine,.cnote,.disc,.small.muted,button,a.btn,table,nav,header,footer,h1,h2,h3,h4,h5,h6,pre,code,.no-justify,[contenteditable],input,textarea,select';
  function run(root) {
    var els = (root || d).querySelectorAll('p,li,dd,blockquote');
    for (var i = 0; i < els.length; i++) {
      var e = els[i];
      if (e.classList.contains('gbj') || e.closest(SKIP)) continue;
      if ((e.textContent || '').trim().length < 100) continue;
      var a = getComputedStyle(e).textAlign;
      if (a === 'left' || a === 'start' || a === 'justify') { e.classList.add('gbj'); bold(e); }
    }
  }
  var KEY = /(₹\s?[\d,]+(?:\.\d+)?(?:\s(?:crore|lakh))?|\bRs\.?\s?[\d,]+|\b\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:\s\d{4})?|\b\d+(?:\.\d+)?%|\b\d+\s(?:working\s)?days?\b)/g;
  function bold(el) {
    var w = d.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), n, list = [];
    while ((n = w.nextNode())) { if (!n.parentNode.closest('b,strong,a,.gbk,del,s') && KEY.test(n.nodeValue)) list.push(n); KEY.lastIndex = 0; }
    list.forEach(function (n) {
      var parts = n.nodeValue.split(KEY), f = d.createDocumentFragment();
      parts.forEach(function (t, i) { if (i % 2) { var b = d.createElement('b'); b.className = 'gbk'; b.textContent = t; f.appendChild(b); } else if (t) f.appendChild(d.createTextNode(t)); });
      n.parentNode.replaceChild(f, n);
    });
  }
  var t;
  function later() { clearTimeout(t); t = setTimeout(run, 150); }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', function () { run(); });
  else run();
  try { new MutationObserver(later).observe(d.documentElement, { childList: true, subtree: true }); } catch (e) {}
})();
