const bar = document.querySelector('.reading-progress');
const links = [...document.querySelectorAll('.chapter-nav a[href^="#"]')];
let queued = false;
function updateProgress() {
  const max = document.documentElement.scrollHeight - innerHeight;
  bar.style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`;
  queued = false;
}
addEventListener('scroll', () => {
  if (!queued) { queued = true; requestAnimationFrame(updateProgress); }
}, { passive: true });
updateProgress();
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
    if (!visible) return;
    links.forEach(link => link.classList.toggle('is-current', link.hash === `#${visible.target.id}`));
  }, { rootMargin: '-12% 0px -68% 0px' });
  document.querySelectorAll('.prd-section').forEach(section => observer.observe(section));
}
