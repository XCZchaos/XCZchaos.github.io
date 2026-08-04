from pathlib import Path
import re
import subprocess

ROOT = Path.cwd()
INDEX = ROOT / "index.html"
STYLES = ROOT / "styles.css"
SCRIPT = ROOT / "script.js"
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def copy_from_backup(source: str, destination: str) -> None:
    target = ASSETS / destination
    target.write_bytes(subprocess.check_output([
        "git", "show", f"origin/backup/full-redesign-20260804:{source}"
    ]))


for src, dst in [
    ("assets/profile.svg", "profile.svg"),
    ("assets/paper.svg", "paper.svg"),
    ("assets/jxau-logo.svg", "jxau-logo.svg"),
    ("assets/csu-logo.svg", "csu-logo.svg"),
    ("assets/resume-data.js", "resume-data.js"),
]:
    copy_from_backup(src, dst)

(ASSETS / "og-cover.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
<defs><linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#070b14"/><stop offset="1" stop-color="#102034"/></linearGradient><linearGradient id="g"><stop stop-color="#63f3cc"/><stop offset=".55" stop-color="#6ba7ff"/><stop offset="1" stop-color="#aa7cff"/></linearGradient></defs>
<rect width="1200" height="630" fill="url(#b)"/><circle cx="940" cy="315" r="190" fill="none" stroke="#63f3cc" stroke-opacity=".18" stroke-width="2"/><circle cx="940" cy="315" r="125" fill="none" stroke="#6ba7ff" stroke-opacity=".28" stroke-width="2"/><path d="M690 340h70l25-100 50 200 42-160 35 60h120" fill="none" stroke="url(#g)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><text x="90" y="230" fill="#f4fbff" font-family="Arial" font-size="76" font-weight="700">Yibo Xiong</text><text x="90" y="310" fill="#63f3cc" font-family="Arial" font-size="44" font-weight="600">Neurotechnology Research Engineer</text><text x="90" y="382" fill="#9fb1c5" font-family="Arial" font-size="28">EEG · fNIRS · Foundation Models · Real-Time BCI Systems</text></svg>''', encoding="utf-8")

html = INDEX.read_text(encoding="utf-8")
if "portrait-orbit" not in html:
    html = html.replace(
        "Yibo Xiong — BCI Algorithm Engineer focused on wearable EEG, multimodal EEG-fNIRS systems, deep learning, and real-time neurotechnology.",
        "Yibo Xiong — Neurotechnology Research Engineer working on wearable EEG, multimodal EEG-fNIRS learning, EEG foundation models, and deployable BCI systems.",
    )
    html = html.replace("Yibo Xiong — BCI Algorithm Engineer", "Yibo Xiong — Neurotechnology Research Engineer")
    html = html.replace("From neural signal acquisition to deployable intelligence.", "Building intelligent systems for brain-computer interfaces.")
    html = html.replace('"jobTitle": "BCI Algorithm Engineer"', '"jobTitle": "Neurotechnology Research Engineer"')
    html = html.replace(
        '        <a href="#research">Research</a>\n        <a href="#contact">Contact</a>',
        '        <a href="#research">Research</a>\n        <a href="#education">Education</a>\n        <a class="nav-cv resume-download" href="#">CV ↓</a>\n        <a href="#contact">Contact</a>',
    )
    html = html.replace("BCI Algorithm Engineer · Incoming M.Eng. Student", "Neurotechnology Research Engineer · Incoming M.Eng. Student")
    html = html.replace(
        '''          <h1>\n            Building intelligence\n            <span class="gradient-text">closer to the brain.</span>\n          </h1>''',
        '''          <h1>\n            Building intelligent systems\n            <span class="gradient-text">for brain–computer interfaces.</span>\n          </h1>''',
    )
    html = html.replace(
        '''            I design full-stack neurotechnology systems that connect\n            <strong>EEG and fNIRS acquisition</strong>, real-time signal processing,\n            multimodal learning, and deployable cognitive-state inference.''',
        '''            I work across the complete BCI pipeline—from <strong>EEG and fNIRS acquisition</strong>\n            to neural representation learning, real-time inference, and deployable\n            neurotechnology systems.''',
    )
    html = html.replace(
        '''            <a class="button button-secondary" href="assets/Yibo_Xiong_Resume.pdf" target="_blank" rel="noopener">\n              View résumé\n            </a>''',
        '''            <a class="button button-secondary resume-download" href="#">Download CV</a>\n            <a class="button button-ghost" href="https://github.com/XCZchaos" target="_blank" rel="noopener">GitHub ↗</a>''',
    )

    visual = re.compile(r'          <div class="orbital-card">.*?          </div>\n        </div>\n      </div>', re.S)
    replacement = '''          <div class="orbital-card portrait-orbit">\n            <img class="hero-portrait" src="assets/profile.svg" alt="Portrait of Yibo Xiong" />\n            <div class="portrait-shade"></div>\n            <div class="orbital-ring ring-one"></div>\n            <div class="orbital-ring ring-two"></div>\n            <div class="portrait-signature"><span>YIBO XIONG</span><strong>Brain · AI · Systems</strong></div>\n            <div class="signal-chip chip-eeg"><span class="chip-dot"></span>EEG<small>electrical</small></div>\n            <div class="signal-chip chip-fnirs"><span class="chip-dot"></span>fNIRS<small>hemodynamic</small></div>\n            <div class="signal-chip chip-ai"><span class="chip-dot"></span>AI<small>representation</small></div>\n            <svg class="wave wave-one" viewBox="0 0 520 140" preserveAspectRatio="none" aria-hidden="true"><path d="M0,74 C25,74 24,74 42,74 C58,74 61,18 73,18 C86,18 88,118 104,118 C120,118 122,54 138,54 C155,54 153,74 173,74 C191,74 195,74 212,74 C228,74 230,39 246,39 C263,39 264,102 279,102 C296,102 299,64 316,64 C334,64 337,74 356,74 C375,74 377,74 398,74 C415,74 419,28 434,28 C449,28 452,112 468,112 C485,112 489,74 520,74"></path></svg>\n            <div class="metric-panel"><div><small>Research</small><strong>EEG Foundation Models</strong></div><div><small>Modalities</small><strong>EEG + fNIRS</strong></div><div><small>Engineering</small><strong>Real-time Systems</strong></div></div>\n          </div>\n        </div>\n      </div>'''
    html, count = visual.subn(replacement, html, count=1)
    if count != 1:
        raise RuntimeError("Hero visual block was not found")

    focus = re.compile(r'          <div class="focus-grid reveal">.*?          </div>\n        </div>', re.S)
    focus_replacement = '''          <div class="focus-grid focus-grid-three reveal">\n            <article class="focus-card"><span>01</span><h3>Neural Signal Intelligence</h3><p>EEG acquisition, artifact-aware preprocessing, interpretable features, and robust neural decoding.</p></article>\n            <article class="focus-card"><span>02</span><h3>Multimodal Brain Computing</h3><p>Temporal alignment and representation fusion for heterogeneous EEG and fNIRS signals.</p></article>\n            <article class="focus-card"><span>03</span><h3>Deployable Neurotechnology</h3><p>EEG foundation models, streaming inference, SDK architecture, and practical research products.</p></article>\n          </div>\n        </div>'''
    html, count = focus.subn(focus_replacement, html, count=1)
    if count != 1:
        raise RuntimeError("Focus block was not found")

    publication = re.compile(r'          <article class="publication-card reveal">.*?          </article>\n\n          <article class="patent-card reveal">', re.S)
    pub_replacement = '''          <article class="publication-card publication-feature reveal">\n            <a class="paper-preview" href="https://doi.org/10.1016/j.bspc.2025.108421" target="_blank" rel="noopener" aria-label="Open CT-MIFNet paper via DOI"><img src="assets/paper.svg" alt="First page of the CT-MIFNet journal paper" /><span>OPEN PAPER ↗</span></a>\n            <div class="publication-copy">\n              <div class="pub-topline"><span>FIRST-AUTHOR PAPER · 2026</span><span>Biomedical Signal Processing and Control</span></div>\n              <h3>CT-MIFNet: Convolutional transformer-based multi-view interaction and fusion network for EEG decoding</h3>\n              <p class="pub-authors"><strong>Yibo Xiong</strong>, Jinming Li, Yun Zhuang, Xiangyue Zhao, Yilu Xu, and Lilin Jie</p>\n              <p>CT-MIFNet combines spatial transformation, multi-scale temporal–frequency–spatial convolution, and Transformer-based feature interaction. Its Cross-Covariance Attention mechanism supports efficient exchange and fusion of multi-view EEG representations.</p>\n              <div class="research-meta"><span>EEG Decoding</span><span>CNN + Transformer</span><span>Multi-View Fusion</span><span>Efficient Attention</span></div>\n              <div class="publication-actions"><a class="button button-primary" href="https://doi.org/10.1016/j.bspc.2025.108421" target="_blank" rel="noopener">Read via DOI ↗</a><a class="button button-secondary" href="https://github.com/XCZchaos/CT-MIFNet" target="_blank" rel="noopener">Source code ↗</a></div>\n            </div>\n          </article>\n\n          <article class="patent-card reveal">'''
    html, count = publication.subn(pub_replacement, html, count=1)
    if count != 1:
        raise RuntimeError("Publication block was not found")

    html = html.replace(
        '''            <article class="education-card reveal">\n              <div class="edu-year">2026 — 2029</div>\n              <div>\n                <p class="project-type">Incoming September 2026</p>\n                <h3>University of Chinese Academy of Sciences</h3>\n                <p>Master of Engineering in Computer Technology</p>\n              </div>\n            </article>''',
        '''            <article class="education-card reveal">\n              <img class="edu-logo" src="assets/csu-logo.svg" alt="Center for Space Utilization, Chinese Academy of Sciences logo" />\n              <div class="edu-year">2026 — 2029</div>\n              <div><p class="project-type">Incoming September 2026</p><h3>University of Chinese Academy of Sciences</h3><p>Master of Engineering in Computer Technology</p><small>Center for Space Utilization, Chinese Academy of Sciences</small></div>\n            </article>''',
    )
    html = html.replace(
        '''            <article class="education-card reveal">\n              <div class="edu-year">2022 — 2026</div>\n              <div>\n                <p class="project-type">Top 30% of major</p>\n                <h3>Jiangxi Agricultural University</h3>\n                <p>Bachelor of Engineering in Software Engineering</p>\n                <small>Coursework: Data Structures & Algorithms, Machine Learning, Artificial Intelligence, Computer Networks, Computer Organization.</small>\n              </div>\n            </article>''',
        '''            <article class="education-card reveal">\n              <img class="edu-logo" src="assets/jxau-logo.svg" alt="Jiangxi Agricultural University logo" />\n              <div class="edu-year">2022 — 2026</div>\n              <div><p class="project-type">Top 30% of major</p><h3>Jiangxi Agricultural University</h3><p>Bachelor of Engineering in Software Engineering</p><small>Coursework: Data Structures & Algorithms, Machine Learning, Artificial Intelligence, Computer Networks, and Computer Organization.</small></div>\n            </article>''',
    )
    html = html.replace(
        '''          <a class="text-link" href="assets/Yibo_Xiong_Resume.pdf" target="_blank" rel="noopener">\n            Open full résumé\n            <span>↗</span>\n          </a>''',
        '''          <a class="text-link resume-download" href="#">Download full résumé <span>↓</span></a>''',
    )
    html = html.replace('  <script src="script.js"></script>', '  <script src="assets/resume-data.js"></script>\n  <script src="script.js"></script>')

INDEX.write_text(html, encoding="utf-8")

css = STYLES.read_text(encoding="utf-8")
marker = "/* Portfolio refinement: original visual language + personal research assets */"
if marker not in css:
    css += r'''

/* Portfolio refinement: original visual language + personal research assets */
.nav-cv{padding:7px 11px;border:1px solid var(--line-strong);border-radius:999px;color:var(--text)!important}.button-ghost{color:var(--muted);border-color:transparent;background:transparent}.portrait-orbit{isolation:isolate}.portrait-orbit::before{z-index:8;pointer-events:none}.portrait-orbit::after{position:absolute;inset:0;z-index:1;content:"";background:linear-gradient(180deg,transparent 55%,rgba(5,9,16,.82) 100%),radial-gradient(circle at 72% 34%,rgba(107,167,255,.12),transparent 38%);pointer-events:none}.hero-portrait{position:absolute;top:70px;right:42px;z-index:2;width:280px;height:350px;max-width:calc(100% - 76px);border:1px solid rgba(255,255,255,.18);border-radius:26px;object-fit:cover;object-position:center;box-shadow:0 28px 70px rgba(0,0,0,.42)}.portrait-shade{position:absolute;top:70px;right:42px;z-index:3;width:280px;height:350px;max-width:calc(100% - 76px);border-radius:26px;background:linear-gradient(180deg,transparent 55%,rgba(4,8,16,.52));pointer-events:none}.portrait-orbit .orbital-ring{z-index:4;opacity:.42;mix-blend-mode:screen}.portrait-orbit .ring-one{top:42%;left:67%;width:246px;height:246px}.portrait-orbit .ring-two{top:42%;left:67%;width:390px;height:205px}.portrait-signature{position:absolute;z-index:6;top:34px;left:36px;display:grid;gap:3px}.portrait-signature span{color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.2em}.portrait-signature strong{font-size:13px;letter-spacing:.02em}.portrait-orbit .signal-chip,.portrait-orbit .wave,.portrait-orbit .metric-panel{z-index:6}.portrait-orbit .chip-eeg{top:132px;left:24px}.portrait-orbit .chip-fnirs{top:228px;right:20px}.portrait-orbit .chip-ai{top:330px;left:28px}.portrait-orbit .wave-one{bottom:112px;opacity:.82}.portrait-orbit .metric-panel{bottom:25px}.focus-grid-three{grid-template-columns:repeat(3,1fr)}.publication-feature{display:grid;min-height:520px;grid-template-columns:280px minmax(0,1fr);align-items:center;gap:34px}.publication-feature::after{display:none}.paper-preview{position:relative;display:block;width:280px;max-width:100%;overflow:hidden;padding:10px;border:1px solid var(--line);border-radius:20px;background:#fff;box-shadow:0 24px 60px rgba(0,0,0,.25);transition:.3s}.paper-preview:hover{border-color:var(--line-strong);transform:translateY(-6px) rotate(-.4deg)}.paper-preview img{display:block;width:280px;max-width:100%;height:auto;object-fit:contain}.paper-preview span{position:absolute;right:20px;bottom:20px;padding:8px 11px;border-radius:999px;color:#06130f;background:var(--accent);font-size:8px;font-weight:900;letter-spacing:.08em}.publication-copy{position:relative;z-index:2}.publication-card .publication-copy h3{margin:30px 0 16px;font-size:clamp(27px,3vw,42px)}.pub-authors{margin-bottom:8px}.pub-authors strong{color:var(--text)}.publication-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}.education-card{grid-template-columns:82px 110px 1fr;gap:20px}.edu-logo{width:76px;height:76px;border:1px solid var(--line);border-radius:50%;object-fit:contain;background:#fff;box-shadow:0 12px 30px rgba(0,0,0,.14)}@media(max-width:1020px){.focus-grid-three{grid-template-columns:1fr}.publication-feature{grid-template-columns:1fr}.paper-preview{width:280px}}@media(max-width:760px){.nav-cv{border:0;border-radius:0}.hero-portrait,.portrait-shade{right:50%;transform:translateX(50%)}.portrait-orbit .chip-ai{display:none}.education-card{grid-template-columns:68px 1fr}.edu-logo{width:62px;height:62px}.edu-year{grid-column:2}.education-card>div:last-child{grid-column:2}}@media(max-width:520px){.hero-portrait,.portrait-shade{top:76px;width:250px;height:313px;max-width:calc(100% - 44px)}.portrait-orbit .chip-fnirs{right:12px}.portrait-orbit .chip-eeg{left:12px}.portrait-signature{left:24px}.publication-card,.patent-card{padding:24px}.paper-preview{padding:8px}}
'''
STYLES.write_text(css, encoding="utf-8")

js = SCRIPT.read_text(encoding="utf-8")
if "function downloadResume" not in js:
    needle = '  document.getElementById("year").textContent = new Date().getFullYear();\n'
    replacement = '''  document.getElementById("year").textContent = new Date().getFullYear();\n\n  function downloadResume(event) {\n    event.preventDefault();\n    const encoded = window.YIBO_RESUME_BASE64;\n    if (!encoded) { alert("The résumé is temporarily unavailable. Please contact asherxiong552@gmail.com."); return; }\n    try {\n      const binary = atob(encoded);\n      const bytes = new Uint8Array(binary.length);\n      for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);\n      const url = URL.createObjectURL(new Blob([bytes], { type: "application/pdf" }));\n      const anchor = document.createElement("a");\n      anchor.href = url; anchor.download = "Yibo_Xiong_Resume.pdf";\n      document.body.appendChild(anchor); anchor.click(); anchor.remove();\n      setTimeout(() => URL.revokeObjectURL(url), 1500);\n    } catch (error) { console.error(error); alert("The résumé could not be downloaded. Please contact asherxiong552@gmail.com."); }\n  }\n  document.querySelectorAll(".resume-download").forEach((link) => link.addEventListener("click", downloadResume));\n'''
    js = js.replace(needle, replacement)
SCRIPT.write_text(js, encoding="utf-8")

Path("README.md").write_text('''# Yibo Xiong — Neurotechnology Portfolio\n\nEnglish academic and engineering portfolio for Yibo Xiong, focused on wearable EEG, multimodal EEG–fNIRS systems, EEG foundation models, and deployable neurotechnology.\n\nLive site: https://xczchaos.github.io/\n''', encoding="utf-8")

required = [
    "portrait-orbit", "publication-feature", "assets/resume-data.js",
    "assets/profile.svg", "assets/paper.svg", "assets/csu-logo.svg", "assets/jxau-logo.svg"
]
final_html = INDEX.read_text(encoding="utf-8")
for token in required:
    if token not in final_html:
        raise RuntimeError(f"Missing required token: {token}")
print("Portfolio refinement complete")
