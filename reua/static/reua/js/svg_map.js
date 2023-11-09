function initActivePoints() {
  const points = JSON.parse(document.getElementById('map_points').textContent);
  points.forEach((point) => {
    const el = document.getElementById(point);
    if (el) el.classList.add('isactive')
  })

}

initActivePoints();