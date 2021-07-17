let map;
var radius = 1;
var radii = 1;
var cntr;
var hexapts = [];
var hexaptsout = [];
var lattosave = [];
var longtosave = [];
var noneed = 0;
var correlation_mthd = 1;

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
    if (radius == "") {
        window.location.reload();
        return alert("Please enter radius");
    } else if (radius <= 0) {
        window.location.reload();
        return alert("Radius should be greater than 0");
    }
    radius = 1000 * radius;
    radii = radius / Math.sqrt(3);
    if (getdates()) {
        return;
    }
    correlation_mthd = document.getElementsByName("corr_mthd")[0];
    correlation_mthd = correlation_mthd.value;
    if (correlation_mthd == "pearson") {
        correlation_mthd = 1;
    } else if (correlation_mthd == "kendall") {
        correlation_mthd = 2;
    } else if (correlation_mthd == "spearman") {
        correlation_mthd = 3;
    } else if (correlation_mthd == "other1") {
        correlation_mthd = 4;
    } else if (correlation_mthd == "other2") {
        correlation_mthd = 5;
    }
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
        document.getElementById('plzwt').style.display = 'block';
        // alert("here");
        postmthd();
        postlati();
        postlongi();
        lattosave = [];
        longtosave = [];
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
            noneed = 0;
        })
    return;

}

function postlongi() {
    $.post(
        url = "/getlongi", // url
        data = { longikey: longtosave }, // data to be submit
        success = function(data) { // success callback
            alert("Your file is ready!!!");
            document.getElementById('plzwt').style.display = 'none';
            document.getElementById('downloadcsv').style.display = 'block';
        })
    return;
}

//convert array to csv
//function artoscv() {
//   csvlat = lattosave.toString();
// csvlong = longtosave.toString();
//document.write(csvlat);
//}
function getdates() {

    var start_date = document.getElementById("startdate").value;
    //end date
    document.getElementById("enddate").setAttribute("max", today);
    var end_date = document.getElementById("enddate").value;
    if (start_date == "" && end_date == "") {
        window.location.reload();
        alert("Please Enter start date and end date");
        return true;
    } else if (start_date == "") {
        window.location.reload();
        alert("Please Enter start date");
        return true;
    } else if (end_date == "") {
        window.location.reload();
        alert("Please Enter end date");
        return true;
    }

    if (start_date >= end_date) {
        window.location.reload();
        alert("start date should be lesser than end date")
        return true;
    }
    if (start_date > "2021-05-31" || end_date > "2021-05-31") {
        window.location.reload();
        alert("Dates violate specified range!")
        return true;
    }

    var dates_array = []
    dates_array.push(start_date);
    dates_array.push(end_date);
    $.post(
        url = "/getstartd", // url
        data = {
            s_d: dates_array
        }, // data to be submit
        success = function(data) { // success callback
            noneed = 0;
        }
    )
    return false;
}

function postmthd() {
    var x = correlation_mthd;
    $.post("/corr_mthd", {
        mthd: x
    });
    /*
    $.post(
        url = "/corr_mthd", // url
        data = {
            mthd: x
        }, // data to be submit
        success = function(data) { // success callback
            noneed = 0;
        }
    )
    */
}

// Restricts input for the given textbox to the given inputFilter.