let map;
var radius = 1;
var radii = 1;
var cntr;
var hexapts = [];
var hexaptsout = [];
var lattosave = [];
var longtosave = [];
//this function will load the map
function loadmap() {
    var mapOptions = {
        center: new google.maps.LatLng(23.5, 78),
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.HYBRID
    };
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    map.setMapTypeId(google.maps.MapTypeId.HYBRID);
}

// this function will assign values and also mark a pt at input location by
//user and also it will store that coordinate to do future processing.
function valueassign() {
    //alert("MARK COORDINATES");
    radius = document.getElementById("radius").value;
    radius = 1000 * radius;
    radii = radius / Math.sqrt(3);
    map.setOptions({
        draggableCursor: "crosshair"
    });
    //use addlistnerfor more than 1 pts and addlistenerOnce for only 1 time
    google.maps.event.addListenerOnce(map, "click", function(e) {
        map.setOptions({
            draggableCursor: ""
        });
        cntr = e.latLng;
        new google.maps.Marker({
            position: cntr,
            map: map
        });
        //this will send for further hexagon making
        generate(cntr);
        //alert("here");
        further();
        map.setCenter(cntr);

        // alert("here");
        postlati();
        postlongi();
    });

}

function markpt(coord) {
    new google.maps.Marker({
        position: coord,
        map: map
    });
    generate(coord);
}

function further() {
    //send to create inner hexagon
    markhexagon(radius, cntr);
    //send to create inner hexagon overlay
    hexagonoverlay(radii);
    //send to create outer hexagon
    markouthexagon((2 * radius), cntr);
    //send to create outer hexagon overlay
    outhexagonoverlay();
}
//inner hexagon pts
function markhexagon(rad, pt) {
    for (var angle = 30; angle < 390; angle += 60) {
        var coord = google.maps.geometry.spherical.computeOffset(
            pt,
            rad,
            angle
        );
        hexapts.push(coord);
        markpt(coord);

    }
    var polygon = new google.maps.Polygon({
        paths: hexapts,
        strokeColor: "#FF0000",
        strokeOpacity: 0.8,
        strokeWeight: 3,
        fillColor: "#F8FCFC",
        fillOpacity: 0.2,
    });
    polygon.setMap(map);
    map.setCenter(cntr);
}
//inner hexagon overlay
function hexagonoverlay(rad) {
    for (var i = 0; i < 6; i++) {
        var b = hexapts[i];
        makehexagon(rad, b);
    }
}
//outer hexagon
function markouthexagon(rad, pt) {
    for (var angle = 30; angle < 390; angle += 60) {
        var coord = google.maps.geometry.spherical.computeOffset(
            pt,
            rad,
            angle
        );
        hexaptsout.push(coord);
        markpt(coord);

    }
    var polygon = new google.maps.Polygon({
        paths: hexaptsout,
        strokeColor: "#FF0000",
        strokeOpacity: 0.8,
        strokeWeight: 3,
        fillColor: "#F8FCFC",
        fillOpacity: 0.2,
    });
    polygon.setMap(map);
    map.setCenter(cntr);
}
//outer hexagon overlay
function outhexagonoverlay() {
    for (var i = 0; i < 6; i++) {
        var b = hexaptsout[i];
        makehexagon(radii, b);
    }
    for (var i = 0; i < 6; i++) {
        var c = google.maps.geometry.spherical.interpolate(
            hexaptsout[i],
            hexaptsout[(i + 1) % 6],
            0.5
        );
        markpt(c);
        makehexagon(radii, c);
        hexaptsout.push(c);
    }
}

function makehexagon(rad, pt) {
    var points = [];
    for (var angle = 0; angle < 360; angle += 60) {
        var coord = google.maps.geometry.spherical.computeOffset(
            pt,
            rad,
            angle
        );
        points.push(coord);
    }

    // Construct the polygon
    var polygon = new google.maps.Polygon({
        paths: points,
        strokeColor: "#FFFF00",
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: "#F8FCFC",
        fillOpacity: 0.1,
    });
    polygon.setMap(map);
    map.setCenter(pt);
}


// saving the file...
function generate(pt) {
    var lati;
    var longi;
    lati = 0;
    longi = 0;
    lati = pt.lat();
    longi = pt.lng();
    lattosave.push(lati);
    longtosave.push(longi);
    return;

}

function postlati() {
    $.post(
        url = "/getlati", // url
        data = { latikey: lattosave }, // data to be submit
        success = function(data) { // success callback
            alert("OK");
        })
    alert("here");
    return;

}

function postlongi() {
    $.post(
        url = "/getlongi", // url
        data = { longikey: longtosave }, // data to be submit
        success = function(data) { // success callback
            alert("OK");
        })
    return;
}

//convert array to csv
//function artoscv() {
//   csvlat = lattosave.toString();
// csvlong = longtosave.toString();
//document.write(csvlat);
//}