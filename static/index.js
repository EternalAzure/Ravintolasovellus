const baseUrl = "https://polar-scrubland-57061.herokuapp.com"
//const baseUrl = "http://localhost:5000"

let map
let restaurants
let markers

const getRestaurants = async () => {
  //Gets restaurants in selected city
  const url = baseUrl + "/api/restaurants"
  const response = await fetch(url, {method: "GET", headers: {"Access-Control-Allow-Origin": baseUrl}})
  return response
}

const getCityLocation = async () => {
  //Gets restaurants in selected city
  const url = baseUrl + "/api/location"
  const response = await fetch(url, {method: "GET", headers: {"Access-Control-Allow-Origin": baseUrl}})
  return response
}

const initMap = async () => {
  console.log("Google maps API initiated")
  restaurants = await (await getRestaurants()).json()
  const myLatLng = await (await getCityLocation()).json()

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: myLatLng,
  })

  infowindow = new google.maps.InfoWindow();

  markers = []
  for (let index = 0; index < restaurants.length; index++) {
    markers[index] = new google.maps.Marker({
      position: restaurants[index].location,
      map,
      title: restaurants[index].name,
      })
      const contentString =
        "<div>" +
        "<a href='"+baseUrl+"/restaurant/"+restaurants[index].id+"'>" +
        "Siirry katsomaan tiedot</a>" +
        "</div>"
      
      markers[index].addListener("click", () => {
        map.setZoom(16);
        map.setCenter(markers[index].getPosition())
        
        infowindow.setContent(contentString)
        infowindow.setPosition(markers[index].getPosition())
        infowindow.open(map)
        //fetch(url, {method: "GET", headers: {"Access-Control-Allow-Origin": baseUrl}})
      })
    
  }
}

const focusOnMap = async (restaurantName) => {
  const index = await findRestaurant(restaurantName)
  if (index < 0) return
  
  map.setZoom(16)
  map.setCenter(markers[index].getPosition())
}

const findRestaurant = async restaurantName => {
  let i = 0
  let res = -1
  await markers.forEach(marker => {
    if (marker.title === restaurantName) {
      res = i
    }
    i++
  });
  return res
}

//This puts the ball rolling
initMap()