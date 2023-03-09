function initInvestitionForm() {
  const isActiveBusines = document.getElementById('id_is_active');
  const container = document.getElementById('investition_turnovers');
  const toggleTurnovers = () => {
    const instance = bootstrap.Collapse.getOrCreateInstance(container);
    if (isActiveBusines.checked) {
      instance.show();
    } else {
      instance.hide();
    }
  }

  isActiveBusines.addEventListener('change', toggleTurnovers);
}

initInvestitionForm();