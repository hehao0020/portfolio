const side = document.querySelector('.side');
const toggle = document.querySelector('.nav-toggle');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (side && toggle) {
  toggle.addEventListener('click', () => {
    const open = side.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  side.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    side.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  }));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && side.classList.contains('open')) {
      side.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
  document.addEventListener('click', event => {
    if (side.classList.contains('open') && !side.contains(event.target) && !toggle.contains(event.target)) {
      side.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}

// Reading progress and section state make long case studies easier to scan.
const progress = document.querySelector('.reading-progress');
let scrollQueued = false;
function syncScroll() {
  const max = document.documentElement.scrollHeight - innerHeight;
  if (progress) progress.style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`;
  scrollQueued = false;
}
addEventListener('scroll', () => {
  if (!scrollQueued) {
    scrollQueued = true;
    requestAnimationFrame(syncScroll);
  }
}, { passive: true });
addEventListener('resize', syncScroll);
syncScroll();

const sectionLinks = [...document.querySelectorAll('.story-index a[href^="#"]')];
const sectionMap = new Map(sectionLinks.map(link => [link.getAttribute('href').slice(1), link]));
if (sectionMap.size && 'IntersectionObserver' in window) {
  const visibleSections = new Map();
  const sectionObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) visibleSections.set(entry.target.id, entry.boundingClientRect.top);
      else visibleSections.delete(entry.target.id);
    });
    const nearest = [...visibleSections].sort((a, b) => Math.abs(a[1]) - Math.abs(b[1]))[0]?.[0];
    if (nearest) sectionLinks.forEach(link => {
      const current = link === sectionMap.get(nearest);
      link.classList.toggle('is-current', current);
      if (current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, { rootMargin: '-12% 0px -58% 0px', threshold: 0 });
  document.querySelectorAll('.story-section[id]').forEach(section => sectionObserver.observe(section));
}

// The cursor light follows the reader only on precise desktop pointers.
if (!reducedMotion && matchMedia('(hover: hover) and (pointer: fine)').matches) {
  document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('pointermove', event => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${event.clientX - rect.left}px`);
      card.style.setProperty('--my', `${event.clientY - rect.top}px`);
    }, { passive: true });
  });
}

if (!reducedMotion && 'IntersectionObserver' in window) {
  const entrance = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('entered');
        entrance.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.project-card, .timeline > div, .mode-grid > div').forEach(item => entrance.observe(item));
}

const lightbox = document.querySelector('.lightbox');
if (lightbox) {
  const image = lightbox.querySelector('img');
  const caption = lightbox.querySelector('p');
  const shots = [...document.querySelectorAll('.shot-open')];
  let currentShot = 0;
  function showShot(index) {
    currentShot = (index + shots.length) % shots.length;
    const button = shots[currentShot];
    image.src = button.dataset.image;
    image.alt = button.querySelector('img')?.alt || '';
    caption.textContent = button.dataset.caption || '';
    lightbox.querySelector('.lightbox-prev').hidden = shots.length < 2;
    lightbox.querySelector('.lightbox-next').hidden = shots.length < 2;
  }
  shots.forEach((button, index) => button.addEventListener('click', () => {
    showShot(index);
    lightbox.showModal();
  }));
  lightbox.querySelector('.lightbox-prev').addEventListener('click', () => showShot(currentShot - 1));
  lightbox.querySelector('.lightbox-next').addEventListener('click', () => showShot(currentShot + 1));
  lightbox.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') showShot(currentShot - 1);
    if (event.key === 'ArrowRight') showShot(currentShot + 1);
  });
  lightbox.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
  lightbox.addEventListener('click', event => { if (event.target === lightbox) lightbox.close(); });
  lightbox.addEventListener('close', () => { image.removeAttribute('src'); });
}

const showcase = document.querySelector('[data-showcase]');
if (showcase) {
  const frames = [...showcase.querySelectorAll('.studio-frame')];
  const tabs = [...showcase.querySelectorAll('[data-show]')];
  const caption = showcase.querySelector('.studio-caption');
  const counter = showcase.querySelector('.studio-counter');
  const play = showcase.querySelector('.studio-play');
  const labels = ['早期探索：从文字到卡片', '三种模式：速度与控制权接力', '当前工作台：写稿、排版、精修'];
  let index = 0;
  let playing = !matchMedia('(prefers-reduced-motion: reduce)').matches;
  let visible = true;
  let timer;
  function show(next) {
    index = next;
    frames.forEach((frame, i) => frame.classList.toggle('is-active', i === index));
    tabs.forEach((tab, i) => {
      tab.classList.toggle('is-active', i === index);
      tab.setAttribute('aria-pressed', String(i === index));
    });
    caption.textContent = labels[index];
    counter.textContent = `0${index + 1} / 03`;
  }
  function schedule() {
    clearInterval(timer);
    if (playing && visible && !document.hidden) timer = setInterval(() => show((index + 1) % frames.length), 4600);
    play.textContent = playing ? '暂停 Ⅱ' : '播放 ▶';
    play.setAttribute('aria-label', playing ? '暂停自动切换' : '播放自动切换');
    play.setAttribute('aria-pressed', String(playing));
  }
  tabs.forEach(tab => tab.addEventListener('click', () => { show(Number(tab.dataset.show)); schedule(); }));
  play.addEventListener('click', () => { playing = !playing; schedule(); });
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; schedule(); }, {threshold: 0.15}).observe(showcase);
  document.addEventListener('visibilitychange', schedule);
  if (!playing) schedule();
}

