from pathlib import Path
import re

ROOT = Path.cwd()
INDEX = ROOT / "index.html"
STYLES = ROOT / "styles.css"

html = INDEX.read_text(encoding="utf-8")

# Simplify navigation labels and make the résumé action visually separate.
old_nav = '''        <a href="#work">Work</a>
        <a href="#research">Research</a>
        <a href="#education">Education</a>
        <a class="nav-cv resume-download" href="#">CV ↓</a>
        <a href="#contact">Contact</a>'''
new_nav = '''        <a href="#work">Projects</a>
        <a href="#research">Publication</a>
        <a href="#education">Education</a>
        <a href="#contact">Contact</a>
        <a class="nav-cv resume-download" href="#">Résumé ↓</a>'''
html = html.replace(old_nav, new_nav)
html = html.replace('<p class="kicker">Selected Work</p>', '<p class="kicker">Selected Projects</p>')
html = html.replace('<p class="kicker">Research Output</p>', '<p class="kicker">Publication & Patent</p>')

# Add browser hints without changing the image fallback behaviour.
html = re.sub(
    r'<img class="hero-portrait"(?![^>]*fetchpriority)',
    '<img class="hero-portrait" fetchpriority="high" decoding="async"',
    html,
)
html = re.sub(
    r'<img src="assets/paper\.webp"(?![^>]*loading)',
    '<img src="assets/paper.webp" loading="lazy" decoding="async"',
    html,
)
html = re.sub(
    r'<img class="edu-logo"(?![^>]*loading)',
    '<img class="edu-logo" loading="lazy" decoding="async"',
    html,
)

INDEX.write_text(html, encoding="utf-8")

css = STYLES.read_text(encoding="utf-8")
marker = "/* Layout polish v2 */"
if marker in css:
    css = css.split(marker, 1)[0].rstrip()

css += r'''

/* Layout polish v2 */
:root {
  --container: 1200px;
}

.section {
  padding: 112px 0;
}

.section-heading {
  grid-template-columns: 64px minmax(0, 1fr);
  align-items: start;
  margin-bottom: 60px;
}

.section-heading h2 {
  max-width: 880px;
}

.nav {
  height: 74px;
  gap: 24px;
}

.nav-links {
  gap: 20px;
}

.nav-links a {
  font-size: 12px;
}

.nav-cv {
  margin-left: 4px;
  padding: 8px 14px;
  border-color: rgba(99, 243, 204, .34);
  color: var(--text) !important;
  background: rgba(99, 243, 204, .06);
}

.nav-cv::after {
  display: none;
}

.hero {
  min-height: auto;
  padding: 134px 0 92px;
}

.hero-grid {
  grid-template-columns: minmax(0, 1.16fr) minmax(390px, .84fr);
  gap: 52px;
}

.hero h1 {
  max-width: 780px;
  margin: 27px 0 22px;
  font-size: clamp(56px, 6.2vw, 88px);
  line-height: .97;
}

.hero-lead {
  max-width: 650px;
}

.hero-actions {
  margin-top: 32px;
}

.button-ghost {
  min-height: 50px;
  padding-inline: 9px;
  color: var(--muted);
}

.hero-meta {
  margin-top: 34px;
}

.orbital-card {
  min-height: 520px;
  border-radius: 32px;
}

.orbital-card::before {
  inset: 15px;
  border-radius: 24px;
}

.hero-portrait {
  top: 56px;
  right: 54px;
  width: 250px;
  height: 311px;
  border-radius: 23px;
  filter: none;
}

.portrait-shade {
  top: 56px;
  right: 54px;
  width: 250px;
  height: 311px;
  border-radius: 23px;
  opacity: .35;
}

.portrait-signature {
  top: 28px;
  left: 30px;
}

.portrait-orbit .ring-one {
  left: 68%;
  width: 226px;
  height: 226px;
  opacity: .32;
}

.portrait-orbit .ring-two {
  left: 68%;
  width: 350px;
  height: 184px;
  opacity: .25;
}

.portrait-orbit .chip-eeg {
  top: 118px;
  left: 20px;
}

.portrait-orbit .chip-fnirs {
  top: 218px;
  right: 16px;
}

.portrait-orbit .chip-ai {
  top: 312px;
  left: 22px;
}

.portrait-orbit .wave-one {
  bottom: 104px;
}

.portrait-orbit .metric-panel {
  bottom: 20px;
}

.stat-strip {
  margin-top: 60px;
}

.stat-strip article {
  min-height: 96px;
}

.about-grid {
  grid-template-columns: 1fr;
  gap: 44px;
}

.about-statement {
  max-width: 930px;
  padding-left: 64px;
}

.focus-grid-three {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.focus-card {
  min-height: 230px;
  padding: 28px;
  background:
    linear-gradient(145deg, rgba(107, 167, 255, .045), transparent 48%),
    var(--panel);
}

.focus-card h3 {
  margin-top: 50px;
}

.timeline {
  max-width: 1090px;
  margin-inline: auto;
}

.timeline-content {
  padding-bottom: 56px;
}

.timeline-content ul {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 28px;
}

.role-heading > span {
  max-width: 220px;
  text-align: center;
}

.project-grid {
  gap: 16px;
}

.project-card {
  min-height: 380px;
  padding: 30px;
  border-radius: 26px;
}

.project-featured {
  min-height: 540px;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.project-graphic {
  min-height: 340px;
}

.project-copy h3 {
  font-size: clamp(25px, 2.7vw, 38px);
}

.research-grid {
  grid-template-columns: 1fr;
  gap: 16px;
}

.publication-feature {
  min-height: auto;
  grid-template-columns: 250px minmax(0, 1fr);
  gap: 46px;
  padding: 40px;
}

.paper-preview,
.paper-preview img {
  width: 250px;
}

.publication-card .publication-copy h3 {
  max-width: 760px;
  margin: 24px 0 15px;
  font-size: clamp(28px, 3.1vw, 42px);
}

.publication-copy > p {
  max-width: 760px;
}

.patent-card {
  display: grid;
  min-height: 0;
  grid-template-columns: 86px minmax(0, 1fr);
  align-items: center;
  gap: 4px 24px;
  padding: 28px 34px;
}

.patent-seal {
  grid-row: 1 / 4;
  margin: 0;
}

.patent-card .project-type,
.patent-card h3,
.patent-card > p:last-child {
  grid-column: 2;
}

.patent-card h3 {
  margin: 4px 0 6px;
}

.patent-card > p:last-child {
  margin: 0;
}

.skills-panel {
  grid-template-columns: .72fr 1.28fr;
  gap: 46px;
  margin-top: 16px;
  padding: 34px;
}

.education-grid {
  grid-template-columns: 1.12fr .88fr;
  gap: 16px;
}

.education-list {
  gap: 16px;
}

.education-card {
  min-height: 190px;
  grid-template-columns: 76px 105px minmax(0, 1fr);
  gap: 20px;
  padding: 28px;
}

.edu-logo {
  width: 68px;
  height: 68px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, .12);
}

.education-card h3 {
  font-size: 23px;
}

.awards-card {
  padding: 30px;
}

.awards-card li {
  padding: 13px 0;
}

.contact-card {
  min-height: 360px;
  grid-template-columns: 1.2fr .8fr;
  align-items: center;
  padding: 46px;
}

.contact-card h2 {
  font-size: clamp(38px, 4.6vw, 60px);
}

@media (max-width: 1020px) {
  .hero-grid {
    grid-template-columns: 1fr;
    gap: 46px;
  }

  .hero-visual {
    width: min(100%, 620px);
    margin-inline: auto;
  }

  .about-statement {
    padding-left: 0;
  }

  .focus-grid-three {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .publication-feature {
    grid-template-columns: 230px minmax(0, 1fr);
    gap: 34px;
  }

  .paper-preview,
  .paper-preview img {
    width: 230px;
  }

  .education-grid,
  .contact-card {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 860px) {
  .focus-grid-three,
  .stat-strip {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .stat-strip article:nth-child(3) {
    border-left: 0;
  }

  .stat-strip article:nth-child(n + 3) {
    border-top: 1px solid var(--line);
  }

  .timeline-content ul {
    grid-template-columns: 1fr;
  }

  .publication-feature {
    grid-template-columns: 1fr;
  }

  .paper-preview {
    margin-inline: auto;
  }

  .patent-card {
    grid-template-columns: 72px minmax(0, 1fr);
  }

  .skills-panel {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .section {
    padding: 88px 0;
  }

  .section-heading {
    grid-template-columns: 42px minmax(0, 1fr);
    margin-bottom: 48px;
  }

  .hero {
    padding: 112px 0 74px;
  }

  .hero h1 {
    font-size: clamp(46px, 12vw, 64px);
  }

  .orbital-card {
    min-height: 490px;
  }

  .hero-portrait,
  .portrait-shade {
    top: 66px;
    right: 50%;
    width: 238px;
    height: 296px;
    transform: translateX(50%);
  }

  .portrait-signature {
    left: 24px;
  }

  .focus-grid-three {
    grid-template-columns: 1fr;
  }

  .project-card {
    min-height: auto;
  }

  .project-featured {
    min-height: auto;
  }

  .education-card {
    grid-template-columns: 62px minmax(0, 1fr);
    gap: 16px;
  }

  .edu-logo {
    width: 58px;
    height: 58px;
  }

  .edu-year,
  .education-card > div:last-child {
    grid-column: 2;
  }

  .contact-card {
    padding: 34px;
  }
}

@media (max-width: 580px) {
  .stat-strip {
    grid-template-columns: 1fr;
  }

  .stat-strip article:nth-child(2) {
    border-top: 1px solid var(--line);
    border-left: 0;
  }

  .project-card,
  .publication-feature,
  .patent-card,
  .skills-panel,
  .awards-card {
    padding: 23px;
  }

  .patent-card {
    grid-template-columns: 58px minmax(0, 1fr);
    gap: 4px 16px;
  }

  .patent-seal svg {
    width: 58px;
  }

  .paper-preview,
  .paper-preview img {
    width: 220px;
  }

  .contact-card {
    padding: 27px;
  }
}
'''

STYLES.write_text(css, encoding="utf-8")
