function initMap() {
  const stations = JSON.parse(document.getElementById('water_stations').textContent);
  let map_center = {lat: 48.272796, lng: 30.31428};
  if (stations && stations.length) {
    map_center = {lat: stations[0].lat, lng: stations[0].lng,};
  }
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 6,
    center: map_center,
  });
  const infoWindow = new google.maps.InfoWindow();
  const stationsList = document.getElementById('water-stations-list');
  stations.forEach(
    (station) => {
      const marker = new google.maps.Marker({
        position: {lat: station.lat, lng: station.lng,},
        map,
        title: station.title,
        optimized: false,
        icon: station.marker,
      })
      const showInfoWindow = () => {
          infoWindow.close();
          infoWindow.setContent(`<div style="max-width: 20rem"><h5>${station.title}</h5><p>${station.desc}</p></div>`);
          infoWindow.open(marker.getMap(), marker);
      }
      if (station.desc) {
        marker.addListener("click", showInfoWindow);
      }
      document.getElementById(`water-station-${station.id}`).addEventListener('click', (e) => {
        stationsList.querySelectorAll('li').forEach((el) => el.classList.remove('active'));
        e.target.classList.add('active');
        showInfoWindow();
      })
    }
  );
}

window.initMap = initMap;
