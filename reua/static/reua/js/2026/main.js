const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const $ = s => document.querySelector(s);

// шапка
function init_header(){
  addEventListener('scroll', () => $('#hdr').classList.toggle('small', scrollY > 40), { passive: true });
}

// поява при прокрутці
function init_scrolls() {
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('in');
      io.unobserve(e.target);
    }
  }), {threshold: .2});
  document.querySelectorAll('.rv, .how').forEach(el => io.observe(el));
}

// ---- карта
function init_maps() {
  const map = document.querySelector('#map');
  console.log();

  const NS = 'http://www.w3.org/2000/svg';
  const M = [[456.6, 162.5, 2, 'Буча, Ворзель'], [634.6, 383.2, 1, 'Кривий Ріг'], [490.3, 499.9, 2, 'Одеса, Одеська обл.'], [435.9, 169.3, 1, 'Макарів'], [703.3, 406.2, 1, 'Марганець'], [792.1, 208.7, 2, 'Харків'], [546.3, 399.1, 1, 'Ольгопіль (Миколаївська обл.)'], [512.7, 490.6, 1, 'Коблеве'], [555.9, 463.9, 3, 'Миколаїв (2), Галицинове'], [532.3, 491.7, 1, 'Очаків'], [475.4, 170.5, 1, 'Київ'], [458.7, 312.9, 1, 'Умань'], [368.7, 217.1, 1, 'Бердичів'], [523.1, 146.0, 1, 'Чернігівська обл.'], [634.1, 78.6, 1, 'Кролевець'], [796.8, 301.2, 1, 'Лозова'], [726.3, 336.8, 1, 'Дніпро'], [862.5, 315.3, 1, 'Олександрівка']];
  const E = [[0, 10], [0, 3], [10, 13], [3, 12], [13, 14], [12, 11], [11, 6], [6, 8], [8, 9], [9, 7], [7, 2], [6, 1], [1, 4], [4, 16], [16, 15], [15, 17], [15, 5]];
  const arcs = $('#arcs'), pts = $('#pts');
  const word = n => n === 1 ? 'станція' : (n < 5 ? 'станції' : 'станцій');
  E.forEach(([a, b], i) => {
    const [x1, y1] = M[a], [x2, y2] = M[b];
    const p = document.createElementNS(NS, 'path');
    p.setAttribute('class', 'arc');
    p.setAttribute('id', 'arc' + i);
    p.setAttribute('d', `M${x1} ${y1} L${x2} ${y2}`);
    arcs.appendChild(p);
    if (!reduce) {
      const c = document.createElementNS(NS, 'circle');
      c.setAttribute('r', 4);
      c.setAttribute('class', 'spark');
      const am = document.createElementNS(NS, 'animateMotion');
      am.setAttribute('dur', (5 + (i % 4)) + 's');
      am.setAttribute('repeatCount', 'indefinite');
      am.setAttribute('begin', (3 + i * .35) + 's');
      const mp = document.createElementNS(NS, 'mpath');
      mp.setAttributeNS('http://www.w3.org/1999/xlink', 'href', '#arc' + i);
      mp.setAttribute('href', '#arc' + i);
      am.appendChild(mp);
      c.appendChild(am);
      c.setAttribute('opacity', 0);
      arcs.appendChild(c);
      am.addEventListener('beginEvent', () => c.setAttribute('opacity', 1));
    }
  });
  M.forEach(([x, y, n, name], i) => {
    const g = document.createElementNS(NS, 'g');
    g.setAttribute('class', 'pt');
    g.style.setProperty('--d', (i * .09) + 's');
    g.style.setProperty('--hd', (i * .2) + 's');
    // іконка станції: маленький контейнер з тінню; число станцій у точці — біла позначка
    g.innerHTML = `<circle class="halo" cx="${x}" cy="${y}" r="20.5"/>`
      + `<image href="${map.dataset.imageStationIcon}" x="${x - 38.8}" y="${y - 21}" width="77.5" height="42"/>`
      + (n > 1 ? `<circle cx="${x + 18.4}" cy="${y - 24.8}" r="12" fill="#fff"/><text x="${x + 18.4}" y="${y - 24.8}">${n}</text>` : '');
    g.addEventListener('mouseenter', () => showTip(g, name, n));
    g.addEventListener('mouseleave', hideTip);
    pts.appendChild(g);
  });
  const tip = $('#tip'), scene = $('#scene');

  function showTip(g, name, n) {
    const r = g.querySelector('image').getBoundingClientRect(), s = scene.getBoundingClientRect();
    tip.querySelector('b').textContent = name;
    tip.querySelector('span').textContent = n + ' ' + word(n);
    tip.style.left = (r.left + r.width / 2 - s.left) + 'px';
    tip.style.top = (r.top - s.top - 6) + 'px';
    tip.classList.add('on');
  }

  function hideTip() {
    tip.classList.remove('on');
  }
}

// послідовність першого екрана
function init_animation_screen() {
  requestAnimationFrame(() => document.body.classList.add('loaded'));
  const map = $('#map');
  setTimeout(() => map.classList.add('pts-on'), reduce ? 0 : 1600);
  setTimeout(() => map.classList.add('arcs-on'), reduce ? 0 : 2600);
  document.querySelectorAll('#hero .rv').forEach(el => el.classList.add('in'));
}

// лічильники
function init_counters() {
  const fmt = n => Math.round(n).toLocaleString('uk-UA');

  function count(el, from, to, dur = 1400) {
    if (reduce) {
      el.textContent = fmt(to);
      return;
    }
    const t0 = performance.now();
    const tick = t => {
      const k = Math.min(1, (t - t0) / dur);
      el.textContent = fmt(from + (to - from) * (1 - Math.pow(1 - k, 3)));
      if (k < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  setTimeout(() => document.querySelectorAll('.stats b').forEach((b, i) => setTimeout(() => count(b, 0, +b.dataset.to), i * 120)), reduce ? 0 : 900);
  const cnum = $('#cnum');
  // лічильник на карті одразу рахує загальну кількість води всіх станцій
  setTimeout(() => count(cnum, 0, 2300000, 1800), reduce ? 0 : 1700);
}

// бульбашки у воді
function init_bublles() {
  if (!reduce) document.querySelectorAll('.bubbles').forEach((bb, k) => {
    for (let i = 0; i < (k ? 9 : 16); i++) {
      const b = document.createElement('i');
      b.className = 'bubble';
      const s = 4 + Math.random() * 8;
      Object.assign(b.style, {
        left: (k ? 12 : 0) + Math.random() * (k ? 82 : 100) + '%',
        width: s + 'px',
        height: s + 'px',
        animationDuration: 9 + Math.random() * 9 + 's',
        animationDelay: -Math.random() * 12 + 's'
      });
      bb.appendChild(b);
    }
  });
}

// кола від курсора на воді
function init_ripples() {
  if (!reduce) document.querySelectorAll('.water').forEach(w => { let last = 0;
    w.addEventListener('pointermove', e => { const now = performance.now(); if (now - last < 120) return; last = now;
      const r = w.getBoundingClientRect(), ring = document.createElement('i'); ring.className = 'ripple';
      ring.style.left = (e.clientX - r.left) + 'px'; ring.style.top = (e.clientY - r.top) + 'px';
      w.appendChild(ring); ring.addEventListener('animationend', () => ring.remove()); }); });
}

function init_footer() {
// великий напис у футері — легкий паралакс
  const big = $('#big');
// розмір шрифту підганяємо під ширину контейнера, щоб напис займав рівно рядок
  const fitBig = () => {
    big.style.fontSize = '100px';
    big.style.fontSize = (100 * (big.parentElement.clientWidth - 80) / big.scrollWidth).toFixed(1) + 'px';
  };
  document.fonts.ready.then(fitBig);
  addEventListener('resize', fitBig);
// під час прокрутки напис «доїжджає» на місце: зсув зменшується до нуля, коли футер повністю на екрані
  if (!reduce) addEventListener('scroll', () => {
    const r = big.getBoundingClientRect();
    const k = Math.max(0, Math.min(1, (r.top - (innerHeight - r.height - 40)) / 400));
    big.style.transform = `translateX(${(k * 90).toFixed(1)}px)`;
  }, {passive: true});
}

// модалка «Напишіть нам»
function init_modal() {
  const modal = $('#feedback_modal');
  const openM = (mdl) => {
    const mbox = mdl.querySelector('.mbox');
    mbox.classList.remove('sent');
    modal.classList.add('open');
    setTimeout(() => mbox.focus(), 300);
  };

  const closeM = () => modal.classList.remove('open');

  document.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-modal-open]');
    if (trigger) {
      const selector = trigger.dataset.modalOpen;
      const element = document.querySelector(selector);
      const offcanvas = document.getElementById('menuOffcanvas');
      if (offcanvas) Offcanvas.getInstance(offcanvas)?.hide();
      openM(element);

    }
  });

  $('#closeM').addEventListener('click', closeM);
  $('#closeM2').addEventListener('click', closeM);
  modal.addEventListener('click', e => {
    if (e.target === modal) closeM();
  });
  addEventListener('keydown', e => {
    if (e.key === 'Escape') closeM();
  });
  $('#mform').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    });
    if (response.redirected){
      mbox.classList.add('sent');
      form.reset();
    } else {
      const data = await response.text();
      form.innerHTML = data;
    }
  });
}

init_header();
init_scrolls();
init_maps();
init_animation_screen();
init_counters();
init_bublles();
init_ripples();
init_footer();
init_modal()