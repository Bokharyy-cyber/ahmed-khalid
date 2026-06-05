// ==================== API CONFIG ====================
const API_BASE_URL = (window.__BOKHARY_API_URL__ || '').replace(/\/$/, '');
const CONTACT_ENDPOINT = API_BASE_URL ? `${API_BASE_URL}/api/contact` : '/api/contact';

// ==================== CURSOR ====================
const cursor = document.getElementById('cursor');
const follower = document.getElementById('cursor-follower');

let mouseX = 0, mouseY = 0;
let followerX = 0, followerY = 0;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  cursor.style.left = mouseX + 'px';
  cursor.style.top = mouseY + 'px';
});

function animateCursor() {
  followerX += (mouseX - followerX) * 0.12;
  followerY += (mouseY - followerY) * 0.12;
  follower.style.left = followerX + 'px';
  follower.style.top = followerY + 'px';
  requestAnimationFrame(animateCursor);
}
animateCursor();

document.querySelectorAll('a, button, .skill-card, .vision-card, .goal-card, .focus-card, .gallery-item').forEach(el => {
  el.addEventListener('mouseenter', () => {
    cursor.style.width = '20px';
    cursor.style.height = '20px';
    cursor.style.background = 'rgba(139,0,0,0.6)';
    follower.style.width = '60px';
    follower.style.height = '60px';
    follower.style.borderColor = 'rgba(139,0,0,0.6)';
  });
  el.addEventListener('mouseleave', () => {
    cursor.style.width = '12px';
    cursor.style.height = '12px';
    cursor.style.background = '#8B0000';
    follower.style.width = '40px';
    follower.style.height = '40px';
    follower.style.borderColor = 'rgba(139,0,0,0.5)';
  });
});

// ==================== LOADER ====================
let percent = 0;
const loaderPercent = document.getElementById('loader-percent');
const barFill = document.getElementById('loader-bar-fill');

const loaderInterval = setInterval(() => {
  percent += Math.random() * 15 + 5;
  if (percent > 100) percent = 100;
  loaderPercent.textContent = Math.round(percent) + '%';
  barFill.style.width = percent + '%';
  if (percent >= 100) clearInterval(loaderInterval);
}, 120);

window.addEventListener('load', () => {
  setTimeout(() => {
    const logo = document.getElementById('loader-logo');
    const line = document.getElementById('loader-line');
    barFill.style.width = '100%';
    loaderPercent.textContent = '100%';
    logo.classList.add('reveal');
    line.classList.add('expand');

    setTimeout(() => {
      const loader = document.getElementById('loader');
      loader.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
      loader.style.opacity = '0';
      loader.style.transform = 'scale(1.05)';
      setTimeout(() => {
        loader.style.display = 'none';
        initHero();
      }, 800);
    }, 1000);
  }, 800);
});

// ==================== HERO ANIMATIONS ====================
function initHero() {
  const tag = document.getElementById('hero-tag');
  const title = document.getElementById('hero-title');
  const subtitle = document.getElementById('hero-subtitle');
  const actions = document.getElementById('hero-actions');
  const word = title.querySelector('.word');

  tag.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
  tag.style.opacity = '1';
  tag.style.transform = 'translateY(0)';

  setTimeout(() => {
    title.style.opacity = '1';
    word.style.transition = 'transform 1.2s cubic-bezier(0.16, 1, 0.3, 1)';
    word.style.transform = 'translateY(0)';
  }, 200);

  setTimeout(() => {
    subtitle.style.transition = 'opacity 0.9s ease, transform 0.9s ease';
    subtitle.style.transform = 'translateY(0)';
    subtitle.style.opacity = '1';
  }, 600);

  setTimeout(() => {
    actions.style.transition = 'opacity 0.9s ease, transform 0.9s ease';
    actions.style.transform = 'translateY(0)';
    actions.style.opacity = '1';
  }, 900);
}

// ==================== PARTICLES ====================
const canvas = document.getElementById('particles-canvas');
const ctx = canvas.getContext('2d');
let particles = [];

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

resizeCanvas();
window.addEventListener('resize', resizeCanvas);

class Particle {
  constructor() {
    this.reset();
  }
  reset() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.size = Math.random() * 1.5 + 0.3;
    this.speed = Math.random() * 0.3 + 0.1;
    this.angle = Math.random() * Math.PI * 2;
    this.drift = (Math.random() - 0.5) * 0.01;
    this.opacity = Math.random() * 0.5 + 0.1;
    this.color = Math.random() > 0.7 ? '139,0,0' : Math.random() > 0.5 ? '10,42,102' : '255,255,255';
  }
  update() {
    this.angle += this.drift;
    this.x += Math.cos(this.angle) * this.speed;
    this.y -= this.speed * 0.5;
    if (this.y < -10) this.reset();
    if (this.x < -10 || this.x > canvas.width + 10) this.reset();
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${this.color}, ${this.opacity})`;
    ctx.fill();
  }
}

for (let i = 0; i < 80; i++) { particles.push(new Particle()); }

function animateParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particles.forEach(p => { p.update(); p.draw(); });
  requestAnimationFrame(animateParticles);
}
animateParticles();

// ==================== SCROLL ====================
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 60) navbar.classList.add('scrolled');
  else navbar.classList.remove('scrolled');
});

// ==================== SCROLL REVEAL ====================
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger').forEach(el => {
  observer.observe(el);
});

// ==================== SKILL BARS ====================
const skillObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('.skill-fill').forEach(bar => {
        const target = bar.dataset.width;
        setTimeout(() => { bar.style.width = target + '%'; }, 200);
      });
    }
  });
}, { threshold: 0.3 });

const skillSection = document.getElementById('skills');
if (skillSection) skillObserver.observe(skillSection);

// ==================== COUNTERS ====================
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('.counter').forEach(counter => {
        const target = parseInt(counter.dataset.target);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        const timer = setInterval(() => {
          current += step;
          if (current >= target) { current = target; clearInterval(timer); }
          counter.textContent = Math.floor(current);
        }, 16);
      });
      counterObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

const achieveSection = document.getElementById('achievements');
if (achieveSection) counterObserver.observe(achieveSection);

// ==================== PARALLAX ====================
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  const heroBg = document.querySelector('.hero-bg-image');
  if (heroBg) {
    heroBg.style.transform = `translateY(${scrollY * 0.3}px)`;
  }
  const orb1 = document.querySelector('.hero-orb-1');
  const orb2 = document.querySelector('.hero-orb-2');
  if (orb1) orb1.style.transform = `translate(${scrollY * 0.05}px, ${scrollY * -0.1}px)`;
  if (orb2) orb2.style.transform = `translate(${scrollY * -0.03}px, ${scrollY * 0.05}px)`;
});

// ==================== MOBILE NAV ====================
let mobileNavOpen = false;

function toggleMobileNav() {
  mobileNavOpen = !mobileNavOpen;
  document.getElementById('mobile-nav').classList.toggle('open', mobileNavOpen);
  const btn = document.getElementById('menu-btn');
  const spans = btn.querySelectorAll('span');
  if (mobileNavOpen) {
    spans[0].style.transform = 'rotate(45deg) translateY(8px)';
    spans[1].style.opacity = '0';
    spans[2].style.transform = 'rotate(-45deg) translateY(-8px)';
  } else {
    spans[0].style.transform = '';
    spans[1].style.opacity = '1';
    spans[2].style.transform = '';
  }
}

function closeMobileNav() {
  mobileNavOpen = false;
  document.getElementById('mobile-nav').classList.remove('open');
  const btn = document.getElementById('menu-btn');
  btn.querySelectorAll('span').forEach(s => {
    s.style.transform = '';
    s.style.opacity = '1';
  });
}

// ==================== CONTACT FORM ====================
async function handleSubmit(e) {
  e.preventDefault();

  const form = document.getElementById('contact-form');
  const status = document.getElementById('form-success');
  const btn = form.querySelector('.form-submit');
  const originalHtml = btn.innerHTML;

  btn.disabled = true;
  btn.innerHTML = '<span>Sending...</span><span>↗</span>';

  try {
    const response = await fetch('https://formspree.io/f/mwvjvvkz', {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    });

    if (!response.ok) throw new Error('Send failed');

    form.reset();
    status.textContent = '✓ Message sent successfully.';
    status.style.display = 'block';
  } catch (err) {
    status.textContent = '⚠ Failed to send message.';
    status.style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.innerHTML = originalHtml;
  }
}

// Add fadeIn keyframe
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .white-05 { color: rgba(255,255,255,0.05); }
  .white-30 { color: rgba(255,255,255,0.3); }
  .white-40 { color: rgba(255,255,255,0.4); }
  .white-60 { color: rgba(255,255,255,0.6); }
  .white-70 { color: rgba(255,255,255,0.7); }
  .white-15 { color: rgba(255,255,255,0.15); }
`;
document.head.appendChild(style);

// ==================== MOUSE PARALLAX HERO ====================
document.getElementById('hero').addEventListener('mousemove', (e) => {
  const rect = document.getElementById('hero').getBoundingClientRect();
  const x = (e.clientX - rect.left) / rect.width - 0.5;
  const y = (e.clientY - rect.top) / rect.height - 0.5;
  const img = document.querySelector('.hero-bg-image');
  if (img) {
    img.style.transform = `translateY(${window.scrollY * 0.3}px) translate(${x * 12}px, ${y * 8}px)`;
  }
});

