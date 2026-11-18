from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:8765/'
PAGES = ['index.html', *[f'projects/{p.stem}.html' for p in sorted((ROOT/'projects').glob('*.html'))],
         *[f'prd/{p.stem}.html' for p in sorted((ROOT/'prd').glob('*.html'))]]
errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
    for width in (390, 1440):
        context = browser.new_context(viewport={'width': width, 'height': 900}, device_scale_factor=1)
        for path in PAGES:
            page = context.new_page()
            page.on('pageerror', lambda error, path=path: errors.append(f'{path}: {error}'))
            page.goto(BASE + path)
            page.wait_for_load_state('load')
            if page.locator('h1').count() != 1:
                errors.append(f'{path}@{width}: h1 count')
            if page.evaluate('document.documentElement.scrollWidth > innerWidth + 3'):
                errors.append(f'{path}@{width}: horizontal overflow')
            for img in page.locator('img').all():
                if not img.get_attribute('src') or not img.is_visible():
                    continue
                img.scroll_into_view_if_needed()
                page.wait_for_timeout(150)
                if not img.evaluate('e => e.complete && e.naturalWidth > 0'):
                    errors.append(f'{path}@{width}: image failed {img.get_attribute("src")}')
            if path == 'index.html':
                rail = page.locator('.home-prd-showcase')
                rail.scroll_into_view_if_needed()
                page.screenshot(path=str(ROOT/'tools'/f'qa-prd-rail-{width}.png'))
                if rail.locator('.prd-rail-card').count() != 14:
                    errors.append(f'rail@{width}: expected 7 cards plus 7 visual copies')
            if path == 'projects/note-studio.html':
                evidence = page.locator('.version-evidence')
                evidence.scroll_into_view_if_needed()
                page.screenshot(path=str(ROOT/'tools'/f'qa-note-versions-{width}.png'))
                evidence.locator('.shot-open').click()
                if not page.locator('.lightbox').evaluate('e => e.open'):
                    errors.append(f'note@{width}: image lightbox did not open')
            if path == 'prd/note-studio.html':
                if 'v1.4.9' not in page.locator('main').inner_text():
                    errors.append('PRD missing latest version')
                page.screenshot(path=str(ROOT/'tools'/f'qa-note-prd-{width}.png'))
            page.close()
        context.close()
    browser.close()

print(f'checked {len(PAGES)} pages at 2 widths')
print('PASS' if not errors else '\n'.join(errors))
if errors:
    raise SystemExit(1)
