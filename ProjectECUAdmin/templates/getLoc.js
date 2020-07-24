var lat = document.getElementById('lat')
var lng = document.getElementById('lng')

if (navigator.geolocation) {
navigator.geolocation.getCurrentPosition(function(position) {
  lat.value = position.coords.latitude;
  lng.value = position.coords.longitude; 
}  