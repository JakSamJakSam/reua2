function initScroll(){
  const header = document.getElementById("header");
  const marker = document.getElementById('header_marker');
  const onScroll = () => {
    if (marker.offsetTop < window.scrollY){
      header.classList.remove('position-absolute');
      header.classList.add('fixed-top', 'bg-deep-purple');
    } else {
      header.classList.add('position-absolute');
      header.classList.remove('fixed-top', 'bg-deep-purple');
    }
  }
  if (header && marker){
    window.addEventListener('scroll', onScroll);
    window.addEventListener('resize', onScroll);
  }
}

function initCoockies(){
  if (!Cookies.get('i_agree_on_cookies')){
    const cookiesToast = document.getElementById('cookiesToast');
    const toast = new bootstrap.Toast(cookiesToast, { autohide: false });
    toast.show();
    const clsoeBtn = cookiesToast.querySelector('[data-bs-dismiss=toast]');
    if (clsoeBtn) {
      clsoeBtn.addEventListener('click', () => {
        Cookies.set('i_agree_on_cookies', true);
        toast.hide()
      });
    }
  }
}

initScroll();
initCoockies();