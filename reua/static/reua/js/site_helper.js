function initScroll() {
  const header = document.getElementById("header");
  const marker = document.getElementById('header_marker');
  const onScroll = () => {
    if (marker.offsetTop < window.scrollY) {
      header.classList.remove('position-absolute');
      header.classList.add('fixed-top', 'bg-deep-purple');
    } else {
      header.classList.add('position-absolute');
      header.classList.remove('fixed-top', 'bg-deep-purple');
    }
  }
  if (header && marker) {
    window.addEventListener('scroll', onScroll);
    window.addEventListener('resize', onScroll);
  }
}

function initCoockies() {
  if (Cookies && !Cookies.get('i_agree_on_cookies')) {
    const cookiesToast = document.getElementById('cookiesToast');
    const toast = new bootstrap.Toast(cookiesToast, {autohide: false});
    toast.show();
    const clsoeBtn = cookiesToast.querySelector('[data-bs-dismiss=toast]');
    if (clsoeBtn) {
      clsoeBtn.addEventListener('click', () => {
        Cookies.set('i_agree_on_cookies', true, {expires: 365});
        toast.hide()
      });
    }
  }
}

function initPaymentModal() {
  if (window.bootstrap) {
    const pbs = document.querySelectorAll('[data-bank_attributes][data-currency]');
    const m = document.getElementById('bank_attributes')
    const modal = new bootstrap.Modal(m);
    modal_currency_header = m.querySelector('#bank_attributes_currency');
    modal_text = m.querySelector('#bank_attributes_text');
    pbs.forEach(pb => {
      pb.addEventListener('click', () => {
        modal_currency_header.innerHTML = pb.dataset['currency'];
        modal_text.innerHTML = pb.dataset['bank_attributes'];
        modal.show(pb);
      })
    })
  }
}

function initLanguages() {
  const items = document.querySelectorAll('.lng');
  items.forEach(item => item.addEventListener('click', (e) => {
    const s = [...item.classList].filter(s => s.startsWith('lng-'));
    const lngName = s.reduce((R, r) => r.replace('lng-', ''), null);
    if (lngName) Cookies.set('django_language', lngName, {expires: 365})
  }));
}

function initCaptcha() {
  const countBlocks = document.querySelectorAll('.captcha_input')
  countBlocks.forEach((cb, idx, parent) => {
    const newDiv = document.createElement("div");
    newDiv.classList.add('captcha_input')
    cb.parentNode.insertBefore(newDiv, cb.nextSibling);
    const elems = cb.querySelectorAll('input,button');
    elems.forEach(el => newDiv.appendChild(el));

  })
}

function submit_feedback_form(...r){
  console.log(r);
}
function initGCaptcha() {
  const captchaButtons = document.querySelectorAll('.g-recaptcha')
  captchaButtons.forEach((button, idx) => {
    fName = `submit_feedback_form-${idx}`;
    window[fName] = function (token) {
      button.form.submit();
    }
    button.dataset.callback = fName;
  });

  }


initScroll();
initCoockies();
// initPaymentModal();
initLanguages();
initCaptcha();
initGCaptcha();