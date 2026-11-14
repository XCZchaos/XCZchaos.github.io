"""Check portfolio structure and optional interactions. Never rewrite the homepage layout."""
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]

class Markup(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.elements = []
        self.feed((ROOT/filename).read_text(encoding='utf-8'))

    def handle_starttag(self, name, attrs):
        self.elements.append((name, dict(attrs)))

    def find(self, tag=None, **attrs):
        return [a for t, a in self.elements if (not tag or t == tag) and all(a.get(k) == v for k,v in attrs.items())]

home, notes = Markup('index.html'), Markup('articles/index.html')
for page in (home, notes):
    assert page.find('button', **{'aria-controls':'site-sections'}) and page.find('div', id='site-sections')
assert home.find('canvas', id='neural-canvas') and home.find('img', **{'class':'hero-portrait'})
assert [a['data-count'] for _,a in home.elements if 'data-count' in a] == ['2','1','1','5']
assert not home.find('figure', **{'class':'signal-plate'})
assert notes.find('details', id='signals')
for name in ('eeg','ppg','fnirs'):
    for key in ('trace','wave','trace-note'):
        assert len(notes.find(**{f'data-{key}':name})) == 1, (key, name)
print('Checked the original homepage layout and the separate signal demo.')
