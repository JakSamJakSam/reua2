document.addEventListener('DOMContentLoaded', function () {
  // =============
  // burdger
  // =============

  var navIcon = document.getElementById('nav-icon1');
  var menuBox = document.getElementById('menubox');

  if (navIcon) {
    navIcon.addEventListener('click', function () {
      navIcon.classList.toggle('open');
      menuBox.classList.toggle('open');
    });
  }
});