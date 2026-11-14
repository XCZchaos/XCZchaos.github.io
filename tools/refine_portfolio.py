"""Validate the publishable branch as it stands. Never copy files from its history."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = set(); self.urls = []; self.notes = []
    def handle_starttag(self, name, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f"Duplicate ID: {attrs['id']}"
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs: self.urls.append(attrs[key])
        if name == 'a' and '/articles/' in attrs.get('href', ''):
            self.notes.append(attrs['href'])
        assert not (name == 'a' and 'download' in attrs), 'Unrequested download action'

if __name__ == '__main__':
    page = Page(); page.feed((ROOT/'index.html').read_text())
    for url in page.urls:
        u = urlsplit(url)
        if u.scheme or u.netloc: continue
        if u.path: assert (ROOT/unquote(u.path).lstrip('/')).is_file(), url
        elif u.fragment: assert u.fragment in page.ids, url
    assert len(set(page.notes)) == 7, 'The complete seven-article series should be linked.'
    assert not any('resume-data' in url.lower() for url in page.urls)
    assert not (ROOT/'assets'/'resume-data.js').exists()
    print('Checked local assets, section anchors, and the article index.')
