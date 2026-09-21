// KCE: page slide direction, phone drawer menu, and the "Recent chats" list.
(function () {

  /* ---------- 1. slide direction between pages (Chrome / Edge 126+) ---------- */
  var ORDER = ['/chat', '/courses', '/departments', '/compare', '/map', '/events', '/emergency'];
  var rank = function (path) { return ORDER.indexOf(path.replace(/\/$/, '') || '/'); };

  window.addEventListener('pageswap', function (e) {
    if (!e.viewTransition || !e.activation || !e.activation.entry) return;
    var to = new URL(e.activation.entry.url).pathname;
    var dir = rank(to) >= rank(location.pathname) ? 1 : -1;
    try { sessionStorage.setItem('kce-dir', String(dir)); } catch (err) {}
  });

  window.addEventListener('pagereveal', function (e) {
    if (!e.viewTransition) return;
    var dir = '1';
    try { dir = sessionStorage.getItem('kce-dir') || '1'; } catch (err) {}
    document.documentElement.style.setProperty('--dir', dir);
  });


  /* ---------- 2. saved chats ---------- */
  var CONV_KEY = 'kce-convos';   // all chats  (localStorage)
  var CUR_KEY = 'kce-chat';      // chat open in this tab (sessionStorage)

  function loadConvos() {
    try { var a = JSON.parse(localStorage.getItem(CONV_KEY) || '[]'); return Array.isArray(a) ? a : []; }
    catch (e) { return []; }
  }
  function saveConvos(list) {
    try { localStorage.setItem(CONV_KEY, JSON.stringify(list.slice(0, 20))); } catch (e) {}
  }
  function currentId() {
    try { return sessionStorage.getItem(CUR_KEY); } catch (e) { return null; }
  }

  function renderRecent() {
    var box = document.getElementById('recent');
    if (!box) return;
    var list = loadConvos();
    var cur = currentId();
    var onChat = document.body.dataset.page === 'chat';
    box.innerHTML = '';
    if (!list.length) {
      var p = document.createElement('p'); p.className = 'recent-empty'; p.textContent = 'Your chats will appear here';
      box.appendChild(p); return;
    }
    list.forEach(function (c) {
      var row = document.createElement('div');
      row.className = 'chat-row' + (onChat && c.id === cur ? ' active' : '');
      var a = document.createElement('a');
      a.href = '/chat?c=' + encodeURIComponent(c.id); a.dataset.chat = c.id;
      a.textContent = c.title; a.title = c.title;
      var d = document.createElement('button');
      d.type = 'button'; d.className = 'chat-del'; d.setAttribute('aria-label', 'Delete chat'); d.textContent = '×';
      d.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        saveConvos(loadConvos().filter(function (x) { return x.id !== c.id; }));
        if (onChat && c.id === cur) {
          if (window.KCE.chat) window.KCE.chat.fresh(); else location.href = '/chat?new=1';
        } else { renderRecent(); }
      });
      row.appendChild(a); row.appendChild(d); box.appendChild(row);
    });
  }

  window.KCE = { CONV_KEY: CONV_KEY, CUR_KEY: CUR_KEY, loadConvos: loadConvos, saveConvos: saveConvos, renderRecent: renderRecent, chat: null };


  /* ---------- 3. phone drawer ---------- */
  var side = document.getElementById('side');
  var scrim = document.getElementById('scrim');
  var menuBtn = document.getElementById('menuBtn');

  function setDrawer(open) {
    if (!side) return;
    side.classList.toggle('open', open);
    if (scrim) scrim.classList.toggle('show', open);
    if (menuBtn) menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) setTimeout(function () { var f = side.querySelector('.newchat'); if (f) f.focus(); }, 60);
    else if (menuBtn && document.activeElement && side.contains(document.activeElement)) menuBtn.focus();
  }

  if (menuBtn) menuBtn.addEventListener('click', function () { setDrawer(!side.classList.contains('open')); });
  if (scrim) scrim.addEventListener('click', function () { setDrawer(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setDrawer(false); });
  if (side) side.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('a')) setDrawer(false); });
  try {
    window.matchMedia('(min-width: 821px)').addEventListener('change', function (e) { if (e.matches) setDrawer(false); });
  } catch (e) {}


  /* ---------- 4. "New chat" / recent chat links: switch in place when already on the chat page ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-chat]');
    if (!a) return;
    if (document.body.dataset.page !== 'chat' || !window.KCE.chat) return;      // other pages: normal link
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    e.preventDefault();
    setDrawer(false);
    if (a.dataset.chat === 'new') window.KCE.chat.fresh(); else window.KCE.chat.open(a.dataset.chat);
  });

  renderRecent();
})();
