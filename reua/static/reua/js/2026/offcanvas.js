class Offcanvas {
  static instances = new Map();
  static active = null;
  static scrollY = 0;

  constructor(element, options = {}) {
    this.element = element;
    this.options = {
      backdrop: true,
      keyboard: true,
      scroll: false,
      ...options
    };

    this.backdrop = null;
    this.isShown = false;
    this.lastFocused = null;

    Offcanvas.instances.set(element, this);
  }

  static getInstance(element) {
    return Offcanvas.instances.get(element);
  }

  static getOrCreateInstance(element, options) {
    return this.getInstance(element) || new Offcanvas(element, options);
  }

  show() {
    if (this.isShown) return;

    if (Offcanvas.active && Offcanvas.active !== this) {
      Offcanvas.active.hide();
    }

    this.isShown = true;
    Offcanvas.active = this;
    this.lastFocused = document.activeElement;

    if (this.options.backdrop) {
      this.backdrop = document.createElement('div');
      this.backdrop.className = 'offcanvas-backdrop';

      document.body.append(this.backdrop);

      this.backdrop.addEventListener('click', () => {
        this.hide();
      });

      // Запускаем CSS-переход
      requestAnimationFrame(() => {
        this.backdrop?.classList.add('show');
      });
    }

    if (!this.options.scroll) {
      Offcanvas.scrollY = window.scrollY;
      document.body.classList.add('offcanvas-open');
    }

    this.element.setAttribute('aria-hidden', 'false');
    this.element.classList.add('show');

    const focusable = this.element.querySelector(
      'button:not(:disabled), a[href], input:not(:disabled), ' +
      'select:not(:disabled), textarea:not(:disabled), ' +
      '[tabindex]:not([tabindex="-1"])'
    );

    (focusable || this.element).focus({preventScroll: true});

    document.addEventListener('keydown', this.onKeydown);
  }

  hide() {
    if (!this.isShown) return;

    this.isShown = false;
    this.element.classList.remove('show');
    this.element.setAttribute('aria-hidden', 'true');

    document.removeEventListener('keydown', this.onKeydown);

    const backdrop = this.backdrop;
    this.backdrop = null;

    if (backdrop) {
      backdrop.classList.remove('show');
      backdrop.addEventListener('transitionend', () => {
        backdrop.remove();
      }, {once: true});

      // На случай отключённых CSS-переходов
      setTimeout(() => backdrop.remove(), 350);
    }

    if (!this.options.scroll) {
      document.body.classList.remove('offcanvas-open');
      window.scrollTo(0, Offcanvas.scrollY);
    }

    if (Offcanvas.active === this) {
      Offcanvas.active = null;
    }

    if (this.lastFocused?.isConnected) {
      this.lastFocused.focus({preventScroll: true});
    }
  }

  toggle() {
    this.isShown ? this.hide() : this.show();
  }

  onKeydown = (event) => {
    if (event.key === 'Escape' && this.options.keyboard) {
      this.hide();
    }

    // Удерживаем Tab внутри открытой панели
    if (event.key === 'Tab') {
      const items = [...this.element.querySelectorAll(
        'a[href], button:not(:disabled), input:not(:disabled), ' +
        'select:not(:disabled), textarea:not(:disabled), ' +
        '[tabindex]:not([tabindex="-1"])'
      )].filter(el => el.getClientRects().length > 0);

      if (!items.length) {
        event.preventDefault();
        this.element.focus();
        return;
      }

      const first = items[0];
      const last = items[items.length - 1];

      if (event.shiftKey &&
        (document.activeElement === first ||
          document.activeElement === this.element)) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey &&
        document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  };
}

// Кнопки открытия
document.addEventListener('click', (event) => {
  const trigger = event.target.closest('[data-offcanvas-toggle]');

  if (trigger) {
    const selector = trigger.dataset.offcanvasToggle;
    const element = document.querySelector(selector);

    if (element) {
      Offcanvas.getOrCreateInstance(element).toggle();
    }
  }

  // Кнопки закрытия внутри панели
  const dismiss = event.target.closest('[data-offcanvas-dismiss]');

  if (dismiss) {
    dismiss.closest('.offcanvas')
    && Offcanvas.getInstance(
      dismiss.closest('.offcanvas')
    )?.hide();
  }
});
