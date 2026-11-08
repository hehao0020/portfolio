const side = document.querySelector('.side');
const toggle = document.querySelector('.nav-toggle');
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

const lightbox = document.querySelector('.lightbox');
if (lightbox) {
  const image = lightbox.querySelector('img');
  const caption = lightbox.querySelector('p');
  document.querySelectorAll('.shot-open').forEach(button => button.addEventListener('click', () => {
    image.src = button.dataset.image;
    image.alt = button.querySelector('img')?.alt || '';
    caption.textContent = button.dataset.caption || '';
    lightbox.showModal();
  }));
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
