"""Validate local navigation, assets, and the seven full articles without modifying the site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FULL_ARTICLES = 'https://xczchaos.shamboo2003.chatgpt.site/articles/'
SLUGS = ('bci', 'eeg', 'preprocessing', 'features', 'cnn', 'transformer', 'sleep')


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.urls = []
        self.full_articles = []
        self.feed(path.read_text(encoding='utf-8'))
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f"Duplicate ID: {attrs['id']}"
            self.ids.add(attrs['id'])
        self.urls.extend(attrs[k] for k in ('href', 'src') if k in attrs)
        if tag == 'a':
            assert 'download' not in attrs, 'Public résumé downloads are disabled'
            if attrs.get('href', '').startswith(FULL_ARTICLES):
                self.full_articles.append(attrs['href'])


if __name__ == '__main__':
    home, notes = ROOT/'index.html', ROOT/'articles/index.html'
    pages = {f: Page(f) for f in (home, notes)}
    for path, page in pages.items():
        for url in page.urls:
            u = urlsplit(url)
            if u.scheme or u.netloc:
                continue
            raw = unquote(u.path)
            target = path if not raw else ((ROOT if raw.startswith('/') else path.parent) / raw.lstrip('/')).resolve()
            if target.is_dir():
                target = target/'index.html'
            assert target.is_relative_to(ROOT) and target.is_file(), (path.name, url)
            if u.fragment and target.suffix == '.html':
                assert u.fragment in pages[target].ids, (path.name, url)
            assert 'resume-data' not in target.name.lower(), url
    assert 'articles/' in pages[home].urls
    assert pages[notes].full_articles == [f'{FULL_ARTICLES}{slug}/' for slug in SLUGS]
    assert not (ROOT/'assets/resume-data.js').exists()
    print('Checked both pages, local image and navigation targets, and all seven full-text URLs.')
