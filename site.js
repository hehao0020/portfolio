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
