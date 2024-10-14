<template>
    <div id="map"></div>
    <div id="div_xy">&nbsp;longitude:-&nbsp;latitude:-&nbsp;</div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-fullscreen/dist/leaflet.fullscreen.css';
import 'leaflet-fullscreen/dist/Leaflet.fullscreen';
import 'leaflet.pm';
import 'leaflet.pm/dist/leaflet.pm.css';
import "leaflet-measure-v2/dist/leaflet-measure";
import "leaflet-measure-v2/dist/leaflet-measure.css";


export default {
    data() {
        return {
        };
    },
    methods: {

    },

    mounted() {
        var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles © Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        });
        var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        });
        var arcgisstreet = L.tileLayer('https://server.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',{
            attribution: 'Tiles © Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        });

        var map = L.map('map', {
            doubleClickZoom:false,
            crs: L.CRS.EPSG3857,
            maxZoom: 18,
            minZoom: 1,
            center: [53.8008, -1.5491],
            zoom: 14,
            layers: [arcgisstreet],
            worldCopyJump: true,
            zoomControl: false,
            attributionControl: false,
            measureControl: false
        });

        var baseLayers = {
            "Esri World Imagery": Esri_WorldImagery,
            "OpenStreetMap": osmLayer,
            "ArcGIS Street": arcgisstreet
        }
        L.control.layers(baseLayers, "", { position: "bottomright" }).addTo(map);
        this.$parent.$data.map = map;

        map.on("mousemove",function(e){
            document.getElementById("div_xy").innerHTML = "&nbsp;Current coordinates:" + e.latlng.lng.toFixed(5) + "," + e.latlng.lat.toFixed(5) + "&nbsp;";
        });
        map.addControl(new window.L.Control.Fullscreen({position:'bottomright'}));

        L.control.scale({position:'bottomleft',maxWidth: '200',metric: true,imperical: false}).addTo(map);

        L.control.zoom({ position: 'bottomright', zoomInTitle: 'Zoom in', zoomOutTitle: 'Zoom out' }).addTo(map);

        map.pm.addControls({
            position: "bottomright",
            drawPolygon: true, 
            drawMarker: false, 
            drawCircleMarker: true, 
            drawPolyline: true, 
            drawRectangle: true, 
            drawCircle: true, 
            editMode: true, 
            dragMode: true, 
            cutPolygon: true, 
            removalMode: true, 
            color: "orange",
            fillColor: "green",
            fillOpacity: 0.4,
        });

        map.on("pm:drawstart", (e) => {
            console.log(e, "Draw the first point");
        });
        map.on("pm:drawend", (e) => {
            console.log(e, "End of drawing");
        });
        map.on("pm:create", (e) => {
            console.log(e, "Called when drawing is complete");
            if (e.shape != 'Marker' && e.shape != 'CircleMarker') {
                if (e.shape == "Circle") {
                    console.log(e.layer._latlng, e.layer._radius, "Plotting coordinates");
                } else {
                    console.log(e.layer._latlngs[0], "Plotting coordinates");
                }
            }

        });
        map.on("pm:globalremovalmodetoggled", (e) => {
            console.log(e, "Called when a layer is cleared");
        });

        var measureControl = L.control.measure({
            position: "bottomright",
            primaryLengthUnit: 'kilometers',
            secondaryLengthUnit: 'meters',
            primaryAreaUnit: 'hectares',
            secondaryAreaUnit: 'sqmeters'
        });
        measureControl.addTo(map);


    }
};

</script>
<style>
#map {
    position:absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
}
#div_xy{
    z-index: 500;
    position: absolute;
    left: 5px;
    bottom: 30px;
    background: rgba(35, 35, 35, 0.7);
    border-radius: 4px;
    font-size: 10pt;
    line-height: 20pt;
    margin: 1pt;
    padding: 1pt;
    color: white;
    border: 0px solid rgb(240, 240, 240);
    font-family: Times New Roman;
}

</style>