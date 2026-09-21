// Chat page: bubbles, typing dots, Markdown replies, conversation memory, and voice.
//   Voice in : mic button (Chrome / Edge) -> speech turned into your question -> sent
//   Voice out: answers to spoken questions are read aloud; every answer has a 🔊 button
// Starts from: ?role=...  |  ?q=...  |  localStorage "initialQuestion" (landing message bar)
(function () {
  var log = document.getElementById('log');
  var form = document.getElementById('askForm');
  var input = document.getElementById('q');
  var sendBtn = document.getElementById('send');
  var chips = document.getElementById('suggest');
  var clearBtn = document.getElementById('clear');
  var micBtn = document.getElementById('mic');
  var langSel = document.getElementById('voiceLang');
  var statusEl = document.getElementById('voiceStatus');
  var KEY = 'kce-chat';
  var WELCOME = log.dataset.welcome || "Hi! I'm KCE AI Assistant 👋\nAsk me anything. Type your question, or tap the 🎤 and speak.";
  var role = log.dataset.role || '';

  var params = new URLSearchParams(location.search);
  var qParam = params.get('q');
  var stored = null;
  try { stored = localStorage.getItem('initialQuestion'); if (stored) localStorage.removeItem('initialQuestion'); } catch (e) {}

  var K = window.KCE || null;
  var convoId = null, convoTitle = null, hist = [];
  var epoch = 0, inflight = null;      // used to drop an answer if you switch chats while waiting

  function newId() { return 'c' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6); }
  function findConvo(id) {
    if (!K || !id) return null;
    var list = K.loadConvos();
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }

  // what to open: a saved chat (?c=), a fresh chat (landing page / ?new=1), or this tab's current chat
  var openParam = params.get('c');
  var newParam = params.get('new');
  if (role || stored || newParam) {
    try { sessionStorage.removeItem(KEY); } catch (e) {}
  } else {
    var want = openParam;
    if (!want) { try { want = sessionStorage.getItem(KEY); } catch (e) {} }
    var found = findConvo(want);
    if (found) {
      convoId = found.id; convoTitle = found.title; hist = found.msgs.slice();
      try { sessionStorage.setItem(KEY, found.id); } catch (e) {}
    }
  }

  function save() {
    if (!K || !hist.length) return;
    if (!convoId) convoId = newId();
    if (!convoTitle) {
      var firstQ = hist.filter(function (m) { return m.who === 'me'; })[0];
      convoTitle = (firstQ ? firstQ.text : 'New chat').replace(/\s+/g, ' ').trim().slice(0, 48);
    }
    var list = K.loadConvos().filter(function (c) { return c.id !== convoId; });
    list.unshift({ id: convoId, title: convoTitle, ts: Date.now(), msgs: hist.slice(-40) });
    K.saveConvos(list);
    try { sessionStorage.setItem(KEY, convoId); } catch (e) {}
    K.renderRecent();
  }
  function now() { return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); }
  function toBottom() { log.scrollTo({ top: log.scrollHeight, behavior: 'smooth' }); }

  /* ================= voice ================= */
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  var synth = window.speechSynthesis;
  var rec = null, listening = false;
  var LANG_KEY = 'kce-voice-lang';

  try { var savedLang = localStorage.getItem(LANG_KEY); if (savedLang) langSel.value = savedLang; } catch (e) {}
  langSel.addEventListener('change', function () { try { localStorage.setItem(LANG_KEY, langSel.value); } catch (e) {} });

  function say(msg, kind) { statusEl.textContent = msg || ''; statusEl.dataset.kind = kind || ''; statusEl.hidden = !msg; }

  function stopSpeaking() {
    if (synth) synth.cancel();
    document.querySelectorAll('.listen.on').forEach(function (b) { b.classList.remove('on'); });
  }

  function plainText(el) {
    var t = el.innerText || el.textContent || '';
    return t.replace(/\p{Extended_Pictographic}/gu, '').replace(/[ \t]+/g, ' ').replace(/\s*\n\s*/g, '. ').trim();
  }

  function chunkText(text) {
    var parts = text.match(/[^.!?।]+[.!?।]*/g) || [text];
    var out = [], cur = '';
    parts.forEach(function (p) {
      if (cur && (cur + p).length > 180) { out.push(cur.trim()); cur = ''; }
      cur += p + ' ';
    });
    if (cur.trim()) out.push(cur.trim());
    return out;
  }

  function pickVoice(lang) {
    var voices = synth.getVoices ? synth.getVoices() : [];
    for (var i = 0; i < voices.length; i++) if (voices[i].lang === lang) return voices[i];
    for (var j = 0; j < voices.length; j++) if (voices[j].lang.indexOf(lang.slice(0, 2)) === 0) return voices[j];
    return null;
  }

  function speak(text, btn) {
    if (!synth || !window.SpeechSynthesisUtterance) return;
    stopSpeaking();
    var clean = text.trim();
    if (!clean) return;
    var lang = /[\u0B80-\u0BFF]/.test(clean) ? 'ta-IN' : (langSel.value === 'ta-IN' ? 'en-IN' : langSel.value);
    var parts = chunkText(clean);
    parts.forEach(function (p, i) {
      var u = new SpeechSynthesisUtterance(p);
      u.lang = lang;
      var v = pickVoice(lang); if (v) u.voice = v;
      if (i === parts.length - 1) u.onend = u.onerror = function () { if (btn) btn.classList.remove('on'); };
      synth.speak(u);
    });
    if (btn) btn.classList.add('on');
  }

  var VOICE_ERRORS = {
    'not-allowed': 'Microphone is blocked. Click the 🔒 icon in the address bar and allow the microphone.',
    'service-not-allowed': 'Microphone is blocked. Click the 🔒 icon in the address bar and allow the microphone.',
    'no-speech': "I didn't hear anything. Tap the 🎤 and try again.",
    'audio-capture': 'No microphone found. Please connect one.',
    'network': 'Voice needs an internet connection (Chrome sends the audio to Google).',
    'language-not-supported': 'This language is not supported for voice in your browser.'
  };

  function startListening() {
    if (!SR) { say('Voice input works in Chrome or Edge. You can still type your question.', 'error'); return; }
    stopSpeaking();
    var finalText = '', hadError = false;
    rec = new SR();
    rec.lang = langSel.value;
    rec.interimResults = true;
    rec.continuous = false;
    rec.maxAlternatives = 1;
    rec.onstart = function () {
      listening = true; micBtn.classList.add('listening'); micBtn.setAttribute('aria-pressed', 'true');
      say('Listening… speak now', 'live');
    };
    rec.onresult = function (e) {
      var t = '';
      for (var i = 0; i < e.results.length; i++) t += e.results[i][0].transcript;
      input.value = t; finalText = t;
    };
    rec.onerror = function (e) {
      hadError = true;
      say(VOICE_ERRORS[e.error] || 'Voice input stopped (' + e.error + '). Please try again.', 'error');
    };
    rec.onend = function () {
      listening = false; micBtn.classList.remove('listening'); micBtn.setAttribute('aria-pressed', 'false');
      var t = finalText.trim();
      if (t && !hadError) { input.value = ''; say(''); ask(t, { voice: true }); }
      else if (!hadError) { say("I didn't hear anything. Tap the 🎤 and try again.", 'error'); }
    };
    try { rec.start(); } catch (e) { say('Could not start the microphone. Please try again.', 'error'); }
  }

  micBtn.addEventListener('click', function () {
    if (listening && rec) { rec.stop(); } else { startListening(); }
  });

  /* ================= chat ================= */
  function fill(bubble, who, text) {
    if (who === 'bot' && window.marked && window.DOMPurify) {
      bubble.innerHTML = DOMPurify.sanitize(marked.parse(text, { breaks: true }));
    } else {
      bubble.textContent = text;
      if (who === 'bot') bubble.style.whiteSpace = 'pre-line';
    }
  }

  function turn(who) {
    var t = document.createElement('div'); t.className = 'turn ' + who;
    if (who === 'bot') { var a = document.createElement('div'); a.className = 'av'; a.textContent = '🤖'; t.appendChild(a); }
    var col = document.createElement('div'); col.className = 'col';
    var bubble = document.createElement('div'); bubble.className = 'bubble';
    col.appendChild(bubble); t.appendChild(col); log.appendChild(t);
    return { turn: t, col: col, bubble: bubble };
  }

  function add(who, text, ts) {
    var m = turn(who);
    fill(m.bubble, who, text);
    var meta = document.createElement('div'); meta.className = 'meta';
    var time = document.createElement('span'); time.className = 'time'; time.textContent = ts || now();
    meta.appendChild(time);
    if (who === 'bot' && synth) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'listen'; b.textContent = '🔊';
      b.title = 'Listen'; b.setAttribute('aria-label', 'Listen to this answer');
      b.addEventListener('click', function () {
        if (b.classList.contains('on')) stopSpeaking(); else speak(plainText(m.bubble), b);
      });
      meta.appendChild(b);
      m.listenBtn = b;
    }
    m.col.appendChild(meta);
    toBottom();
    return m;
  }

  function typing() {
    var m = turn('bot');
    m.bubble.innerHTML = '<span class="dots"><i></i><i></i><i></i></span>';
    toBottom();
    return m.turn;
  }

  async function ask(text, opts) {
    text = (text || '').trim();
    if (!text) return;
    stopSpeaking();
    chips.hidden = true;
    var ts = now();
    add('me', text, ts); hist.push({ who: 'me', text: text, ts: ts });

    // earlier messages, so follow-up questions make sense
    var earlier = hist.slice(-9, -1).map(function (m) {
      return { role: m.who === 'me' ? 'user' : 'assistant', content: m.text };
    });

    save();                                   // the question shows up in "Recent chats" straight away
    var myEpoch = epoch;
    var dots = typing();
    input.disabled = true; sendBtn.disabled = true; micBtn.disabled = true;
    var reply;
    var ctrl = new AbortController();
    inflight = ctrl;
    try {
      var timer = setTimeout(function () { ctrl.abort(); }, 90000);
      var r = await fetch('/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history: earlier }), signal: ctrl.signal
      });
      clearTimeout(timer);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      reply = (await r.json()).reply;
    } catch (e) {
      reply = 'Sorry, I could not reach the server. Please try again.';
    }
    if (myEpoch !== epoch) return;            // you opened another chat meanwhile: ignore this answer
    inflight = null;
    dots.remove();
    ts = now();
    var m = add('bot', reply, ts); hist.push({ who: 'bot', text: reply, ts: ts }); save();
    input.disabled = false; sendBtn.disabled = false; micBtn.disabled = false;
    if (opts && opts.voice) speak(plainText(m.bubble), m.listenBtn);   // spoke the question -> hear the answer
    else input.focus();
  }

  // draw the current conversation (or the greeting + suggestions for an empty one)
  function showHistory() {
    log.innerHTML = '';
    if (hist.length) {
      chips.hidden = true;
      hist.forEach(function (m) { add(m.who, m.text, m.ts); });
    } else {
      chips.hidden = false;
      add('bot', WELCOME);
    }
  }

  function switchTo(c) {
    epoch++;
    if (inflight) { inflight.abort(); inflight = null; }
    stopSpeaking(); say('');
    input.disabled = false; sendBtn.disabled = false; micBtn.disabled = false;
    if (c) {
      convoId = c.id; convoTitle = c.title; hist = c.msgs.slice();
      try { sessionStorage.setItem(KEY, c.id); } catch (e) {}
    } else {
      convoId = null; convoTitle = null; hist = [];
      try { sessionStorage.removeItem(KEY); } catch (e) {}
    }
    showHistory();
    if (K) K.renderRecent();
    input.focus();
  }

  // used by the sidebar / drawer ("New chat" and "Recent chats") without reloading the page
  if (K) K.chat = {
    fresh: function () { switchTo(null); },
    open: function (id) { switchTo(findConvo(id)); }
  };

  showHistory();

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = input.value; input.value = ''; ask(v);
  });
  document.querySelectorAll('[data-q]').forEach(function (b) {
    b.addEventListener('click', function () { ask(b.dataset.q); });
  });
  clearBtn.addEventListener('click', function () { switchTo(null); });
  window.addEventListener('pagehide', stopSpeaking);

  // keep the address bar clean (refresh will not re-run the role / question)
  if (role || qParam || newParam || openParam) { try { history.replaceState(null, '', location.pathname); } catch (e) {} }

  var first = qParam || stored;
  if (first) ask(first); else input.focus();
})();
