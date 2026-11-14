"""Export the JPEGs already embedded in the public SVG assets without recompressing."""
from pathlib import Path
import base64
import xml.etree.ElementTree as ET

assets = Path(__file__).resolve().parents[1] / 'assets'
for source, target in [('profile','portrait'),('paper','paper-cover'),('csu-logo','csu-mark'),('jxau-logo','jxau-mark')]:
    node = ET.parse(assets / (source + '.svg')).find('.//{http://www.w3.org/2000/svg}image')
    url = next(value for value in node.attrib.values() if value.startswith('data:image/jpeg;base64,'))
    data = base64.b64decode(url.split(',', 1)[1], validate=True)
    dest = assets / (target + '.jpg')
    if not dest.exists() or dest.read_bytes() != data:
        dest.write_bytes(data)
