/* ===== Chin-En Gau — shared site script ===== */
const REEL_ID = 'Kb7IJWt5PzY';   // YouTube video ID of the reel
const REEL_START = 15;           // start second
const REEL_END   = 209;          // stop here (3:29), fade out, then restart

/* language toggle (remembered per browser) */
const langBtn = document.getElementById('lang');
function setLang(l){
  document.documentElement.lang = l;
  if (langBtn) langBtn.textContent = l === 'zh' ? 'EN' : '中文';
  try { localStorage.setItem('lang', l); } catch(e) {}
}
try { if (localStorage.getItem('lang') === 'zh') setLang('zh'); } catch(e) {}
if (langBtn) langBtn.addEventListener('click', () => setLang(document.documentElement.lang === 'zh' ? 'en' : 'zh'));

/* mobile menu */
const menu = document.getElementById('menu'), burger = document.getElementById('burger');
if (burger) burger.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  document.querySelector('.nav').classList.toggle('menuopen', open);
  burger.textContent = open ? 'Close' : 'Menu';
});
if (menu) menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  menu.classList.remove('open'); document.querySelector('.nav').classList.remove('menuopen');
  if (burger) burger.textContent = 'Menu';
}));

/* modal: reel with sound / lightbox */
const modal = document.getElementById('modal'), box = document.getElementById('modalbox');
function openModal(html){ box.innerHTML = html; modal.classList.add('open'); document.body.style.overflow = 'hidden'; }
function closeModal(){ modal.classList.remove('open'); box.innerHTML = ''; document.body.style.overflow = ''; }
if (modal) {
  document.getElementById('closemodal').addEventListener('click', closeModal);
  modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });
  addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
  document.querySelectorAll('[data-reel]').forEach(b => b.addEventListener('click', e => {
    e.preventDefault();
    openModal(`<iframe src="https://www.youtube.com/embed/${REEL_ID}?autoplay=1&start=${REEL_START}&rel=0" allow="autoplay; fullscreen" allowfullscreen frameborder="0"></iframe>`);
  }));
  document.querySelectorAll('.gallery img').forEach(img => img.addEventListener('click', () => openModal(`<img src="${img.src}" alt="">`)));
}

/* scroll reveal */
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .1 });
document.querySelectorAll('.rv').forEach(el => io.observe(el));
document.querySelectorAll('#yr').forEach(el => el.textContent = new Date().getFullYear());

/* ===== hero background reel =====
   Preferred: a short silent self-hosted loop (assets/reel-loop.mp4).
   A plain <video muted loop> has no player UI at all, and muted autoplay is
   allowed by every browser - so no play/pause overlay can ever appear.
   If that file is missing we fall back to the YouTube embed. */
const ytwrap = document.getElementById('ytwrap'),
      curtain = document.getElementById('curtain'),
      bgvid   = document.getElementById('bgvid');

if (ytwrap) {
  let handled = false;
  const reveal = () => curtain.classList.add('off');
  const cover  = () => curtain.classList.remove('off');

  function sizeBg(){
    const w = innerWidth, h = innerHeight;
    let vw = w, vh = w * 9 / 16; if (vh < h) { vh = h; vw = h * 16 / 9; }
    ytwrap.style.width = (vw * 1.06) + 'px'; ytwrap.style.height = (vh * 1.06) + 'px';
  }
  sizeBg(); addEventListener('resize', sizeBg);

  /* ---- fallback: YouTube embed, kept hidden until frames actually roll ---- */
  function startYouTube(){
    if (handled) return; handled = true;
    const tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    document.head.appendChild(tag);
    window.onYouTubeIframeAPIReady = function(){
      let restarting = false;
      const p = new YT.Player('ytbg', { videoId: REEL_ID,
        playerVars: { autoplay:1, mute:1, controls:0, start:REEL_START, playsinline:1,
                      rel:0, modestbranding:1, iv_load_policy:3, disablekb:1, fs:0 },
        events: {
          onReady: e => { e.target.mute(); e.target.playVideo(); },
          onStateChange: e => {
            const S = YT.PlayerState;
            if (e.data !== S.PLAYING) cover();
            if (e.data === S.ENDED && !restarting) { e.target.seekTo(REEL_START); e.target.playVideo(); }
          }
        }});
      setInterval(() => {
        let t, st;
        try { t = p.getCurrentTime(); st = p.getPlayerState(); } catch (err) { return; }
        if (restarting) return;
        if (t >= REEL_END) {
          restarting = true; cover();
          setTimeout(() => { try { p.seekTo(REEL_START); p.playVideo(); } catch (err) {} restarting = false; }, 950);
          return;
        }
        if (t < REEL_START - 0.5) { try { p.seekTo(REEL_START); } catch (err) {} return; }
        if (st === YT.PlayerState.PLAYING && t > REEL_START + 0.35) reveal();
      }, 200);
    };
  }

  /* ---- preferred: the self-hosted silent loop ---- */
  if (bgvid) {
    bgvid.muted = true; bgvid.defaultMuted = true;
    bgvid.src = 'assets/reel-loop.mp4';

    bgvid.addEventListener('playing', () => {
      handled = true;
      bgvid.classList.add('on');
      reveal();
      // if the fallback had already been started, drop it - the loop wins
      const f = document.querySelector('#ytwrap iframe');
      if (f) f.remove();
    }, { once: true });

    // retry play() once enough has buffered (the first call can be too early)
    bgvid.addEventListener('canplay', () => { const a = bgvid.play(); if (a && a.catch) a.catch(() => {}); });
    bgvid.addEventListener('error', () => startYouTube());

    const attempt = bgvid.play();
    if (attempt && attempt.catch) attempt.catch(() => {});   // wait for canplay instead of bailing

    // only fall back if nothing is loading at all - a slow download is not a failure
    setTimeout(() => {
      if (handled) return;
      if (bgvid.networkState === 2 /* LOADING */ || bgvid.readyState >= 2) return;
      startYouTube();
    }, 9000);
  } else {
    startYouTube();
  }
}
