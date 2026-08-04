(() => {
  const root = document.documentElement;
  const header = document.querySelector('.site-header');
  const themeToggle = document.querySelector('.theme-toggle');
  const menuToggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  const pointer = document.querySelector('.pointer-light');
  const portrait = document.querySelector('.portrait-card');
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) root.dataset.theme = savedTheme;
  else if (matchMedia('(prefers-color-scheme: light)').matches) root.dataset.theme = 'light';

  themeToggle?.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    localStorage.setItem('theme', next);
  });

  menuToggle?.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(open));
  });

  document.querySelectorAll('.nav-links a').forEach(link => link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    menuToggle?.setAttribute('aria-expanded', 'false');
  }));

  const onScroll = () => header?.classList.toggle('scrolled', scrollY > 24);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    });
  }, { threshold: .12 });
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  const navItems = [...document.querySelectorAll('.nav-links a')];
  const sectionObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navItems.forEach(link => link.classList.toggle('active', link.hash === `#${entry.target.id}`));
    });
  }, { rootMargin: '-35% 0px -55% 0px' });
  document.querySelectorAll('main section[id]').forEach(section => sectionObserver.observe(section));

  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = Number(el.dataset.count);
      const start = performance.now();
      const animate = now => {
        const p = Math.min((now - start) / 850, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(animate);
      };
      requestAnimationFrame(animate);
      counterObserver.unobserve(el);
    });
  }, { threshold: .8 });
  document.querySelectorAll('[data-count]').forEach(el => counterObserver.observe(el));

  function downloadResume(event) {
    event.preventDefault();
    const encoded = window.YIBO_RESUME_BASE64;
    if (!encoded) {
      alert('The résumé file is temporarily unavailable. Please contact asherxiong552@gmail.com.');
      return;
    }
    try {
      const binary = atob(encoded);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
      const url = URL.createObjectURL(new Blob([bytes], { type: 'application/pdf' }));
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = 'Yibo_Xiong_Resume.pdf';
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1500);
    } catch (error) {
      console.error(error);
      alert('The résumé could not be downloaded. Please contact asherxiong552@gmail.com.');
    }
  }
  document.querySelectorAll('.resume-download').forEach(link => link.addEventListener('click', downloadResume));

  if (!reduceMotion) {
    addEventListener('pointermove', event => {
      if (pointer) pointer.style.transform = `translate(${event.clientX - 170}px, ${event.clientY - 170}px)`;
    }, { passive: true });

    portrait?.addEventListener('pointermove', event => {
      const box = portrait.getBoundingClientRect();
      const x = (event.clientX - box.left) / box.width - .5;
      const y = (event.clientY - box.top) / box.height - .5;
      portrait.style.transform = `rotateX(${-y * 4}deg) rotateY(${x * 6}deg)`;
    });
    portrait?.addEventListener('pointerleave', () => portrait.style.transform = 'rotateX(0) rotateY(0)');
  }

  document.getElementById('year').textContent = new Date().getFullYear();

  const canvas = document.getElementById('network-canvas');
  if (!canvas || reduceMotion) return;
  const ctx = canvas.getContext('2d');
  let width, height, nodes;

  function resize() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    width = innerWidth;
    height = innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.min(82, Math.max(34, Math.floor(width * height / 24000)));
    nodes = Array.from({ length: count }, () => ({
      x: Math.random() * width, y: Math.random() * height,
      vx: (Math.random() - .5) * .16, vy: (Math.random() - .5) * .16,
      r: Math.random() * 1.3 + .5
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);
    const light = root.dataset.theme === 'light';
    const nodeColor = light ? '25,119,105' : '95,240,199';
    const lineColor = light ? '31,76,88' : '120,174,190';
    nodes.forEach((node, index) => {
      node.x += node.vx; node.y += node.vy;
      if (node.x < 0 || node.x > width) node.vx *= -1;
      if (node.y < 0 || node.y > height) node.vy *= -1;
      ctx.beginPath(); ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${nodeColor},.36)`; ctx.fill();
      for (let j = index + 1; j < nodes.length; j++) {
        const other = nodes[j];
        const distance = Math.hypot(node.x - other.x, node.y - other.y);
        if (distance < 125) {
          ctx.beginPath(); ctx.moveTo(node.x, node.y); ctx.lineTo(other.x, other.y);
          ctx.strokeStyle = `rgba(${lineColor},${(1 - distance / 125) * .13})`;
          ctx.lineWidth = .7; ctx.stroke();
        }
      }
    });
    requestAnimationFrame(draw);
  }
  resize();
  addEventListener('resize', resize, { passive: true });
  draw();
})();