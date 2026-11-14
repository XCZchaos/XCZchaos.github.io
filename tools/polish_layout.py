"""Validate the maintained layout without regenerating or truncating site styles."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
source = (root/'index.html').read_text()
for file in re.findall(r'<link\b[^>]*?href="([^"?#]+\.css)(?:\?[^"]*)?"', source):
    assert (root/file).is_file(), file
for name in ('eeg', 'ppg', 'fnirs'):
    for role in ('trace', 'wave', 'trace-note'):
        assert source.count(f'data-{role}="{name}"') == 1, (role, name)
assert 'aria-controls="site-sections"' in source and 'id="site-sections"' in source
print('Checked signal selections and navigation controls.')
