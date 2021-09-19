
const getAll = async () => {
  const url = "http://localhost:5000/api/restaurants"
  const response = await fetch(url)

  return response
}

async function initMap () {
  const restaurants = await (await getAll()).json()
  
  const myLatLng = { lat: 60.1699, lng: 24.9384 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: myLatLng,
  });

  restaurants.forEach(r => {
    new google.maps.Marker({
    position: r.location,
    map,
    title: r.name,
    });
  });
  
}
