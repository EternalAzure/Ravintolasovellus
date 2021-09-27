const baseUrl = "https://polar-scrubland-57061.herokuapp.com"
const headers = new Headers();
headers.append("Access-Control-Allow-Origin", baseUrl);


const getRestaurants = async () => {
  console.log("getRestaurants")
  //Gets restaurants in selected city
  const url = baseUrl + "/api/restaurants"
  const response = await fetch(url, {method: "GET", headers: {"Access-Control-Allow-Origin": baseUrl}})
  return response
}

const getCityLocation = async () => {
  console.log("getLocation")
  //Gets restaurants in selected city
  const url = baseUrl + "/api/location"
  const response = await fetch(url, {method: "GET", headers: {"Access-Control-Allow-Origin": baseUrl}})
  return response
}

const initMap = async () => {
  console.log("Google maps API initiated")
  const restaurants = await (await getRestaurants()).json()
  const myLatLng = await (await getCityLocation()).json()   // { lat: 60.1699, lng: 24.9384 };
  console.log("myLatLng:", myLatLng)

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: myLatLng,
  })

  infowindow = new google.maps.InfoWindow();

  let markers = []
  for (let index = 0; index < restaurants.length; index++) {
    markers[index] = new google.maps.Marker({
      position: restaurants[index].location,
      map,
      title: restaurants[index].name,
      })
      
      markers[index].addListener("click", () => {
        map.setZoom(16);
        map.setCenter(markers[index].getPosition());
      })
    
  }
}

//This puts the ball rolling
initMap()