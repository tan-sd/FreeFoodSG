var script = document.createElement('script');
script.src = 'https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap';
script.async = true;

// get the user's location from their wifi connection / mobile data.

// copy and paste the code below to get the location of the user when they open the site.

// call getLocation() to get coordinates of the user into two variables, latitude and longtitude.
function get_location() {
    console.log("get location function is running") // for troubleshooting
    // console.log(x) // for troubleshooting
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(show_position);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
function show_position(position) {
    var latitude = position.coords.latitude 
    var longitude = position.coords.longitude;
    var geocoder = new google.maps.Geocoder()
    var location  = new google.maps.LatLng(latitude, longitude);    // turn coordinates into an object          
    geocoder.geocode({'location':location}, function(results, status) {
        if(status == google.maps.GeocoderStatus.OK){
            var address = results[0]["formatted_address"]
            console.log(address)
            get_routing_url(address)
        }
        document.getElementById("location").innerHTML = "latitude = " + latitude + "<br>" + "longitude = " + longitude + "<br>" + "address:" + address
    })
}

// assuming you have the destination as a address
function get_routing_url(destination) {
    var url = "https://maps.google.com?saddr=Current+Location&daddr=" + destination
    document.getElementById("routing_url").innerHTML = "<a href='" + url + "'>click me</a>"
}

// data-login_uri="login.html"

// function onSignIn(googleUser) {
//     var profile = googleUser.getBasicProfile();
//     console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
//     console.log('Name: ' + profile.getName());
//     console.log('Image URL: ' + profile.getImageUrl());
//     console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
//   } 

function decodeJwtResponse(jwt) {
    return jwt_decode(jwt);
}

function onSignIn(response) {
    console.log(decodeJwtResponse(response.credential))
    
    responsePayload = decodeJwtResponse(response.credential)

    console.log("ID: " + responsePayload.sub);
    console.log('Full Name: ' + responsePayload.name);
    console.log('Given Name: ' + responsePayload.given_name);
    console.log('Family Name: ' + responsePayload.family_name);
    console.log("Image URL: " + responsePayload.picture);
    console.log("Email: " + responsePayload.email);
  } 