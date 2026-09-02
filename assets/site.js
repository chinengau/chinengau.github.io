/* ===== Chin-En Gau — shared site script ===== */
const REEL_ID = 'Kb7IJWt5PzY';   // YouTube video ID of the reel
const REEL_START = 15;           // start second

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
if (burger) burger.addEventListener('click', () => menu.classList.toggle('open'));

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

/* looping background reel on the home page */
const ytbg = document.getElementById('ytbg');
if (ytbg) {
  function sizeBg(){
    const w = innerWidth, h = innerHeight;
    let vw = w, vh = w * 9 / 16; if (vh < h) { vh = h; vw = h * 16 / 9; }
    ytbg.style.width = (vw * 1.06) + 'px'; ytbg.style.height = (vh * 1.06) + 'px';
  }
  sizeBg(); addEventListener('resize', sizeBg);
  const tag = document.createElement('script'); tag.src = 'https://www.youtube.com/iframe_api'; document.head.appendChild(tag);
  window.onYouTubeIframeAPIReady = function(){
    const p = new YT.Player('ytbg', { videoId: REEL_ID,
      playerVars: { autoplay:1, mute:1, controls:0, start:REEL_START, loop:1, playlist:REEL_ID, playsinline:1, rel:0, modestbranding:1, iv_load_policy:3, disablekb:1, fs:0 },
      events: {
        onReady: e => { e.target.mute(); e.target.playVideo(); },
        onStateChange: e => {
          if (e.data === YT.PlayerState.PLAYING) document.getElementById('ytbg').classList.add('on');
          if (e.data === YT.PlayerState.ENDED) { e.target.seekTo(REEL_START); e.target.playVideo(); }
        }
      }});
    setInterval(() => { try { if (p.getCurrentTime() < REEL_START - .5) p.seekTo(REEL_START); } catch(e) {} }, 1000);
  };
}
