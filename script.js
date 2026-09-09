(() => {
  const doc = document.documentElement;
  const header = document.querySelector(".site-header");
  const themeToggle = document.querySelector(".theme-toggle");
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");
  const cursorGlow = document.querySelector(".cursor-glow");
  const orbitalCard = document.querySelector(".orbital-card");
  const scrollProgress = document.querySelector(".scroll-progress span");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const savedTheme = localStorage.getItem("theme");
  if (savedTheme) {
    doc.dataset.theme = savedTheme;
  } else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
    doc.dataset.theme = "light";
  }

  themeToggle?.addEventListener("click", () => {
    const next = doc.dataset.theme === "dark" ? "light" : "dark";
    doc.dataset.theme = next;
    localStorage.setItem("theme", next);
  });

  navToggle?.addEventListener("click", () => {
    const open = navLinks.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(open));
  });

  document.querySelectorAll(".nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
      navToggle?.setAttribute("aria-expanded", "false");
    });
  });

  const handleScroll = () => {
    header?.classList.toggle("scrolled", window.scrollY > 24);
    if (scrollProgress) {
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      const ratio = maxScroll > 0 ? Math.min(window.scrollY / maxScroll, 1) : 0;
      scrollProgress.style.transform = `scaleX(${ratio})`;
    }
  };
  window.addEventListener("scroll", handleScroll, { passive: true });
  handleScroll();

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

  const sections = [...document.querySelectorAll("main section[id]")];
  const navItems = [...document.querySelectorAll(".nav-links a")];

  const sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navItems.forEach((link) => {
          link.classList.toggle("active", link.getAttribute("href") === `#${entry.target.id}`);
        });
      });
    },
    { rootMargin: "-35% 0px -55% 0px" }
  );
  sections.forEach((section) => sectionObserver.observe(section));

  const counters = document.querySelectorAll("[data-count]");
  const counterObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = Number(el.dataset.count);
        const start = performance.now();
        const duration = 900;

        const tick = (now) => {
          const progress = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          el.textContent = String(Math.round(target * eased));
          if (progress < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        counterObserver.unobserve(el);
      });
    },
    { threshold: 0.8 }
  );
  counters.forEach((counter) => counterObserver.observe(counter));

  if (!reduceMotion) {
    window.addEventListener("pointermove", (event) => {
      if (cursorGlow) {
        cursorGlow.style.transform = `translate(${event.clientX - 160}px, ${event.clientY - 160}px)`;
      }
    }, { passive: true });

    orbitalCard?.addEventListener("pointermove", (event) => {
      const rect = orbitalCard.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      orbitalCard.style.transform = `rotateX(${-y * 5}deg) rotateY(${x * 7}deg)`;
    });

    orbitalCard?.addEventListener("pointerleave", () => {
      orbitalCard.style.transform = "rotateX(0deg) rotateY(0deg)";
    });
  }

  document.getElementById("year").textContent = new Date().getFullYear();

  const pipelineData = {
    align: {
      index: "01",
      title: "Multimodal acquisition and alignment",
      copy: "Synchronize EEG, fNIRS, behavioral events, and stimulus markers through unified timestamps and offset compensation, creating a dependable input for downstream analysis.",
      evidence: "Evidence: research platform · emotion experiment platform",
    },
    clean: {
      index: "02",
      title: "Signal preprocessing and quality control",
      copy: "Build filtering, segmentation, baseline correction, artifact suppression, and quality-check pipelines that convert noisy physiological recordings into consistent algorithm inputs.",
      evidence: "Evidence: EEG/fNIRS preprocessing · adaptive online filtering",
    },
    learn: {
      index: "03",
      title: "Interpretable features and deep learning",
      copy: "Combine physiological features with multimodal representation learning, then train and evaluate models for cognitive state, sleep state, and emotion recognition tasks.",
      evidence: "Evidence: feature fusion · lightweight classifiers · PyTorch training",
    },
    serve: {
      index: "04",
      title: "Real-time inference and reusable interfaces",
      copy: "Connect trained models and signal algorithms to stable C/C++ cores, Windows FFI, Android JNI/NDK, and application services with validation and lifecycle controls.",
      evidence: "Evidence: Windows SDK · Android AAR · real-time headband inference",
    },
    deliver: {
      index: "05",
      title: "Algorithms translated into product value",
      copy: "Shape technical capabilities around user workflows so researchers receive reproducible experiments, developers receive reusable APIs, and analysis teams receive interpretable reports.",
      evidence: "Evidence: research workflow · SDK delivery · report productization",
    },
  };

  const pipelineDetail = document.querySelector(".pipeline-detail");
  document.querySelectorAll(".pipeline-stage").forEach((button) => {
    button.addEventListener("click", () => {
      const data = pipelineData[button.dataset.stage];
      if (!data || !pipelineDetail) return;
      document.querySelectorAll(".pipeline-stage").forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-pressed", String(active));
      });
      pipelineDetail.innerHTML = `<span>SELECTED STAGE · ${data.index}</span><div><h4>${data.title}</h4><p>${data.copy}</p></div><strong>${data.evidence}</strong>`;
      pipelineDetail.classList.remove("detail-flash");
      requestAnimationFrame(() => pipelineDetail.classList.add("detail-flash"));
    });
  });

  const newsData = {
    competition: {
      date: "SEP 2026 · OPEN",
      title: "Open to BCI competition collaboration",
      copy: "Welcoming team invitations involving physiological signal algorithms, multimodal learning, real-time inference, or BCI system development.",
      link: "mailto:asherxiong552@gmail.com?subject=BCI%20Competition%20Collaboration",
      action: "Discuss collaboration ↗",
    },
    paper: {
      date: "2026 · PUBLICATION",
      title: "First-author EEG decoding paper published",
      copy: "CT-MIFNet was published in Biomedical Signal Processing and Control, presenting convolutional Transformer-based multi-view interaction and fusion for EEG decoding.",
      link: "https://doi.org/10.1016/j.bspc.2025.108421",
      action: "Read the paper ↗",
    },
    patent: {
      date: "SEP 2025 · GRANTED",
      title: "Chinese invention patent granted",
      copy: "The EEG-based emotion-recognition result visualization method and system received authorization under patent ZL 2025 1 0102267.X.",
      link: "#research",
      action: "View patent details ↓",
    },
  };

  const newsDetail = document.querySelector(".news-feed-detail");
  document.querySelectorAll(".news-feed-tab").forEach((button) => {
    button.addEventListener("click", () => {
      const data = newsData[button.dataset.news];
      if (!data || !newsDetail) return;
      document.querySelectorAll(".news-feed-tab").forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-selected", String(active));
      });
      newsDetail.innerHTML = `<span class="news-feed-date">${data.date}</span><h3>${data.title}</h3><p>${data.copy}</p><a href="${data.link}"${data.link.startsWith("http") ? ' target="_blank" rel="noopener"' : ""}>${data.action}</a>`;
    });
  });

  const metricData = {
    eeg: ["EEG METRICS", "Quantifies neural rhythms, peak alpha frequency, and frontal alpha asymmetry for interpretable brain-function summaries."],
    fnirs: ["fNIRS METRICS", "Transforms hemoglobin dynamics into HbO, HbR, HbT, integral, centroid, and activation indicators for regional hemodynamic interpretation."],
    hrv: ["AUTONOMIC METRICS", "Summarizes beat-to-beat variation through time- and frequency-domain HRV indicators to complement brain-signal analysis."],
    coupling: ["COUPLING METRICS", "Uses cross-correlation strength and delay to characterize temporal relationships between electrical and hemodynamic activity."],
  };

  const metricDetail = document.querySelector(".metric-detail");
  document.querySelectorAll(".metric-option").forEach((button) => {
    button.addEventListener("click", () => {
      const data = metricData[button.dataset.metric];
      if (!data || !metricDetail) return;
      document.querySelectorAll(".metric-option").forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-pressed", String(active));
      });
      metricDetail.innerHTML = `<span>${data[0]}</span><p>${data[1]}</p>`;
    });
  });

  const projectCards = [...document.querySelectorAll(".project-card[data-project-tags]")];
  const projectCount = document.querySelector(".project-count");
  document.querySelectorAll(".project-filter").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;
      let visible = 0;
      document.querySelectorAll(".project-filter").forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-pressed", String(active));
      });
      projectCards.forEach((card) => {
        const match = filter === "all" || card.dataset.projectTags.split(" ").includes(filter);
        card.hidden = !match;
        if (match) visible += 1;
      });
      if (projectCount) projectCount.textContent = `${visible} project${visible === 1 ? "" : "s"}`;
    });
  });

  const projectData = {
    sdk: {
      type: "DEVELOPER ENABLEMENT · 2026",
      title: "Cross-Platform Physiological Signal Algorithm SDK",
      summary: "Reusable physiological-signal algorithms for Windows and Android application teams.",
      situation: "Desktop and Android teams needed to reuse EEG, fNIRS, HR/HRV, preprocessing, metrics, and signal-quality algorithms, but interfaces and platform behavior were inconsistent.",
      task: "Own the SDK architecture and core development, while defining stable contracts between application code, platform adapters, native bindings, and signal algorithms.",
      action: "Abstracted shared C/C++ modules; implemented Windows FFI and Android JNI/NDK integration; standardized validation, error codes, state semantics, warm-up, abnormal-input handling, and resource release.",
      result: "Delivered Windows SDK and Android AAR packages with a unified calculation and integration contract, reducing repeated wrapping and cross-platform adaptation for downstream developers.",
      stack: "C/C++ · TypeScript/Node.js · Java/Kotlin · FFI · JNI/NDK · DLL · AAR",
    },
    "research-platform": {
      type: "RESEARCH WORKFLOW · 2026",
      title: "EEG-fNIRS Multimodal Cognitive State Research Platform",
      summary: "A unified acquisition-to-prediction workflow designed around researchers' daily experiments.",
      situation: "Researchers faced fragmented acquisition tools, difficult cross-modal alignment, and repeated manual work when moving from raw recordings to cognitive-state results.",
      task: "Build a reusable platform that joined synchronized acquisition, experiment management, preprocessing, deep-learning inference, and result visualization.",
      action: "Designed timestamp alignment and offset compensation; implemented filtering, segmentation, baseline correction, quality checks, feature fusion, model training/evaluation, and service integration with Go, Vue, and ECharts.",
      result: "Delivered a reusable acquisition–alignment–analysis–prediction workflow that reduced cross-software processing and created a consistent data foundation for cognitive-load, sleep, and future model iteration.",
      stack: "Python · PyTorch · EEG/fNIRS · Go/Gin/GORM · Vue · ECharts",
    },
    "emotion-platform": {
      type: "MOTION BCI · RESEARCH PROTOTYPE",
      title: "Motion-BCI Emotion Experiment & Quantification Platform",
      summary: "Real-time emotion experimentation and visualization for motion-oriented BCI scenarios.",
      situation: "Emotion during motion-oriented BCI experiments was difficult to quantify objectively and present to researchers in real time.",
      task: "Create the full technical chain from emotion-induction paradigms and synchronized EEG acquisition to recognition and quantitative display.",
      action: "Developed experimental paradigms and LSL markers; designed adaptive online filtering, differential entropy, band power, alpha lateralization, a lightweight classifier, real-time inference, and visualization.",
      result: "Delivered a prototype validated in participant sessions and supported real-time model execution on an EEG headband, turning algorithm output into directly readable emotion information.",
      stack: "Python · LSL · EEG preprocessing · Feature engineering · Deep learning · Real-time visualization",
    },
    "medical-platform": {
      type: "CLINICAL-ANALYSIS WORKFLOW · 2026",
      title: "EEG-fNIRS Multimodal Medical Assistive Analysis Platform",
      summary: "Interpretable multimodal metrics and report workflows for brain-function analysis scenarios.",
      situation: "Raw EEG, fNIRS, and cardiac signals needed to become consistent, computable, interpretable results that could support hospital-oriented validation and report analysis.",
      task: "Design and develop the core preprocessing and indicator algorithms, then connect reference rules, visual summaries, abnormal prompts, and report-ready conclusions.",
      action: "Implemented EEG/fNIRS denoising, segmentation, baseline correction, quality checks, and alignment; designed EEG, hemodynamic, HRV, and cross-modal coupling indicators; supported report logic and visualization.",
      result: "Completed the product loop from preprocessing and metric calculation to interpretation and reporting, enabling quantitative brain-function summaries, abnormal prompts, and explainable analysis outputs.",
      stack: "Python · EEG/fNIRS preprocessing · EEG spectral metrics · HRV · CCF coupling · Report productization",
    },
  };

  const projectDialog = document.querySelector(".project-dialog");
  let dialogTrigger = null;
  document.querySelectorAll("[data-project-open]").forEach((button) => {
    button.addEventListener("click", () => {
      const data = projectData[button.dataset.projectOpen];
      if (!data || !projectDialog) return;
      dialogTrigger = button;
      projectDialog.querySelector(".dialog-type").textContent = data.type;
      projectDialog.querySelector("#dialog-title").textContent = data.title;
      projectDialog.querySelector(".dialog-summary").textContent = data.summary;
      projectDialog.querySelectorAll("[data-dialog-field]").forEach((field) => {
        field.textContent = data[field.dataset.dialogField];
      });
      projectDialog.querySelector(".dialog-stack").textContent = data.stack;
      if (typeof projectDialog.showModal === "function") projectDialog.showModal();
      else projectDialog.setAttribute("open", "");
      document.body.classList.add("dialog-open");
      projectDialog.querySelector(".dialog-close").focus();
    });
  });

  function closeProjectDialog() {
    if (!projectDialog) return;
    if (typeof projectDialog.close === "function") projectDialog.close();
    else projectDialog.removeAttribute("open");
  }
  projectDialog?.querySelector(".dialog-close")?.addEventListener("click", closeProjectDialog);
  projectDialog?.addEventListener("click", (event) => {
    if (event.target === projectDialog) closeProjectDialog();
  });
  projectDialog?.addEventListener("close", () => {
    document.body.classList.remove("dialog-open");
    dialogTrigger?.focus();
  });

  const toast = document.querySelector(".site-toast");
  let toastTimer = null;
  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("visible"), 2200);
  }
  document.querySelectorAll("[data-copy-email]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(button.dataset.copyEmail);
        showToast("Email copied to clipboard");
      } catch {
        showToast("Email: asherxiong552@gmail.com");
      }
    });
  });

  const canvas = document.getElementById("neural-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  let width = 0;
  let height = 0;
  let nodes = [];
  let rafId = null;

  function resizeCanvas() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const count = Math.min(90, Math.max(36, Math.floor((width * height) / 22000)));
    nodes = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.17,
      vy: (Math.random() - 0.5) * 0.17,
      r: Math.random() * 1.4 + 0.6,
    }));
  }

  function drawNetwork() {
    ctx.clearRect(0, 0, width, height);
    const isLight = doc.dataset.theme === "light";
    const lineColor = isLight ? "18, 62, 98" : "120, 169, 218";
    const nodeColor = isLight ? "21, 111, 103" : "99, 243, 204";

    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i];
      node.x += node.vx;
      node.y += node.vy;

      if (node.x < 0 || node.x > width) node.vx *= -1;
      if (node.y < 0 || node.y > height) node.vy *= -1;

      ctx.beginPath();
      ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${nodeColor}, .38)`;
      ctx.fill();

      for (let j = i + 1; j < nodes.length; j++) {
        const other = nodes[j];
        const dx = node.x - other.x;
        const dy = node.y - other.y;
        const distance = Math.hypot(dx, dy);

        if (distance < 125) {
          ctx.beginPath();
          ctx.moveTo(node.x, node.y);
          ctx.lineTo(other.x, other.y);
          ctx.strokeStyle = `rgba(${lineColor}, ${(1 - distance / 125) * 0.12})`;
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }
    }
    rafId = requestAnimationFrame(drawNetwork);
  }

  resizeCanvas();
  window.addEventListener("resize", resizeCanvas, { passive: true });

  if (!reduceMotion) {
    drawNetwork();
  } else {
    drawNetwork();
    cancelAnimationFrame(rafId);
  }
})();
