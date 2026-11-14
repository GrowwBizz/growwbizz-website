/* GrowwBizz: justified, hyphenated paragraphs. Also on phones (hyphenation keeps gaps small). Skips centred/right text, headings, buttons, tables, labels. */
(function () {
  var d = document, s = d.createElement('style');
  s.textContent = '.gbj{text-align:justify;text-justify:inter-word;hyphens:auto;-webkit-hyphens:auto;overflow-wrap:break-word}';
  d.head.appendChild(s);
  if (!d.documentElement.lang) d.documentElement.lang = 'en';
  var SKIP = '.meta,.src,.fine,.cnote,.disc,.small.muted,button,a.btn,table,nav,header,footer,h1,h2,h3,h4,h5,h6,pre,code,.no-justify,[contenteditable],input,textarea,select';
  function run(root) {
    var els = (root || d).querySelectorAll('p,li,dd,blockquote');
    for (var i = 0; i < els.length; i++) {
      var e = els[i];
      if (e.classList.contains('gbj') || e.closest(SKIP)) continue;
      if ((e.textContent || '').trim().length < 40) continue;
      var a = getComputedStyle(e).textAlign;
      if (a === 'left' || a === 'start' || a === 'justify') e.classList.add('gbj');
    }
  }
  var t;
  function later() { clearTimeout(t); t = setTimeout(run, 150); }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', function () { run(); });
  else run();
  try { new MutationObserver(later).observe(d.documentElement, { childList: true, subtree: true }); } catch (e) {}
})();
