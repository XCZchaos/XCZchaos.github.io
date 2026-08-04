from pathlib import Path

root = Path.cwd()
index_path = root / "index.html"
styles_path = root / "styles.css"

html = index_path.read_text(encoding="utf-8")

replacements = {
    'src="assets/profile.svg"': 'src="assets/profile.webp" onerror="this.onerror=null;this.src=\'assets/profile.svg\'"',
    'src="assets/paper.svg"': 'src="assets/paper.webp" onerror="this.onerror=null;this.src=\'assets/paper.svg\'"',
    'src="assets/jxau-logo.svg"': 'src="assets/jxau.webp" onerror="this.onerror=null;this.src=\'assets/jxau-logo.svg\'"',
    'src="assets/csu-logo.svg"': 'src="assets/csu.webp" onerror="this.onerror=null;this.src=\'assets/csu-logo.svg\'"',
}
for old, new in replacements.items():
    html = html.replace(old, new)

index_path.write_text(html, encoding="utf-8")

css = styles_path.read_text(encoding="utf-8")
marker = "/* Image quality correction */"
if marker not in css:
    css += r'''

/* Image quality correction */
.portrait-orbit {
  transform: none !important;
}
.hero-portrait {
  width: 248px;
  height: 309px;
  right: 58px;
  image-rendering: auto;
  backface-visibility: hidden;
  filter: contrast(1.025) saturate(1.025);
}
.portrait-shade {
  width: 248px;
  height: 309px;
  right: 58px;
  opacity: .44;
}
.paper-preview {
  width: 246px;
}
.paper-preview img {
  width: 246px;
  image-rendering: auto;
  backface-visibility: hidden;
}
.paper-preview:hover {
  transform: translateY(-4px);
}
.edu-logo {
  image-rendering: auto;
  backface-visibility: hidden;
}
@media (max-width: 760px) {
  .hero-portrait,
  .portrait-shade {
    right: 50%;
    transform: translateX(50%);
  }
}
'''
styles_path.write_text(css, encoding="utf-8")
