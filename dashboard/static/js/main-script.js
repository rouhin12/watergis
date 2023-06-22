$(document).ready(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() > 50) {
            $('.navbar').addClass('navbar-scrolled');
        } else {
            $('.navbar').removeClass('navbar-scrolled');
        }
    });

    $('.navbar-toggler').click(function () {
        $('.navbar-collapse').toggleClass('navbar-expanded');
    });
});
var mymap;
var source = L.wms.source(
    "https://geoserver2.communitygis.net/geoserver/wms",
    {
        "format": "image/png",
        "transparent": "true"
    }
);

mymap = L.map('mapdiv', {
    center: [19.0760, 84.8777],
    zoom: 5, zoomControl: false,
    attributionControl: false,
    messagebox: true,
    contextmenu: true,
    measureControl: false
});
mymap.messagebox.options.timeout = 5000;
mymap.messagebox.setPosition("bottomright");
lyrOSM = L.tileLayer.provider('OpenStreetMap.Mapnik');
lyrOSM2 = L.tileLayer.provider('OpenStreetMap.Mapnik');
lyrImagery = L.tileLayer.provider('Esri.WorldImagery');
let tiles = new L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});

mymap.addLayer(tiles);
var miniMap = new L.Control.MiniMap(lyrOSM2, { toggleDisplay: true }).addTo(mymap);
//  var miniMap = new L.Control.MiniMap(lyrOSM).addTo(mymap);

function round(value, precision) {
    var multiplier = Math.pow(10, precision || 0);
    return Math.round(value * multiplier) / multiplier;
}


function copyToClipboard(text) {
    var dummy = document.createElement("textarea");
    // dummy.style.display = 'none'
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);
}

mymap.on('contextmenu', function (e) {
    copyToClipboard(e.latlng.lat + "," + e.latlng.lng);
    mymap.messagebox.show("<h6>Latitude:<b>" + round(e.latlng.lat, 4) + "</b> Longitude:<b>" + round(e.latlng.lng, 4) + "</b> copied to clipboard</h6>");
});



$('.select').click(function () {
    $(this).toggleClass('highlight')
})



$("#closebutton").click(function () {
    ctlSidebar.toggle();
});



objBasemaps = {
    "Open Street Maps": lyrOSM,
    "Imagery": lyrImagery
};

objOverlays = {
};

// var ctlLayers = L.control.layers(objBasemaps, objOverlays).addTo(mymap);
var ctlSidebar = L.control.sidebar('side-bar').addTo(mymap);
// var ctlPan = L.control.pan().addTo(mymap);

var ctlEasybutton = L.easyButton('fa fa fa-bars', function () {
    ctlSidebar.toggle();
}).addTo(mymap);
ctlSidebar.show();

var ctlZoomslider = L.control.zoomslider({ position: 'topright' }).addTo(mymap);

ctlAttribute = L.control.attribution({ position: 'bottomleft' }).addTo(mymap);