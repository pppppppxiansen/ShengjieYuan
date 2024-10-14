<template>
    <div id="road">
        <el-button-group>
            <el-button type="info" v-for="item in items" :key="item" @click="btnClickEvt(item)">
                {{ item }}
            </el-button>
        </el-button-group>
    </div>
    <div class="div_dialog" id="div_searchLocation">
        <div class="div_dialog_header">Location query
            <img @click="closeLocationDlg" src="../assets/images/delete.png">
        </div>
        <div class="div_dialog_body">
            &nbsp;&nbsp;&nbsp;&nbsp;longitude:&nbsp;<input type="text" id="txt_search_lng" value="-1.5491"
                size="12px">&nbsp;&nbsp;&nbsp;&nbsp;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;latitude:&nbsp;<input type="text" id="txt_search_lat" value="53.8008"
                size="12px">&nbsp;&nbsp;&nbsp;&nbsp;<br>
            <button @click="setLocation">&nbsp;&nbsp;Query&nbsp;&nbsp;</button>
        </div>
    </div>
    <div class="div_dialog" id="div_levelLocation">
        <div class="div_dialog_header">&nbsp;Zoom level
            <img @click="closeLevelDlg" src="../assets/images/delete.png">
        </div>
        <div class="div_dialog_body">
            &nbsp;&nbsp;&nbsp;&nbsp;Zoom level:&nbsp;<input type="text" id="txt_level_lng" value="13"
                size="12px">&nbsp;&nbsp;&nbsp;&nbsp;<br>
            <button @click="setMapLevel">&nbsp;&nbsp;Confirm&nbsp;&nbsp;</button>
        </div>
    </div>
</template>

<script>
    import L from 'leaflet';
    import 'leaflet/dist/leaflet.css';
    import 'leaflet-routing-machine';
    import $ from 'jquery';

    export default {
        data() {
            return {
                items: ['Show Roads', 'Clean', 'Start', 'End', 'Calculate Path','Location query','Reset','Zoom level','Scope','Pixel','Information'],
                geojsonLayer: null,
                map: null,
                startPoint: null,
                endPoint: null,
                routingControl: null,
                heatmapLayer: null,
            };
        },
        mounted() {
            this.map = this.$parent.$data.map; 
            this.initListeners();
        },
        methods: {
            btnClickEvt(item) {
                switch (item) {
                    case 'Show Roads':
                        this.showRoads();
                        break;
                    case 'Clean':
                        this.cleanMap();
                        break;
                    case 'Start':
                        this.setStartPoint();
                        break;
                    case 'End':
                        this.setEndPoint();
                        break;
                    case 'Calculate Path':
                        this.calculatePath();
                        break;
                    case 'Location query':
                        this.showLocationDlg();
                        break;
                    case 'Reset':
                        this.restore();
                        break;
                    case 'Zoom level':
                        this.showLevelDlg();
                        break;
                    case 'Scope':
                        this.showMapRange();
                        break;
                    case 'Pixel':
                        this.showMapPixel();
                        break;
                    case 'Information':
                        this.showMapInfo();
                        break;

                }
            },
            showRoads() {
                if (!this.geojsonLayer) {
                    $.ajax({
                        url: process.env.BASE_URL + "static/data/road.geojson?t=" + new Date().getTime(),
                        success: (result) => {
                            this.geojsonLayer = L.geoJSON(result, {
                                style: () => ({ color: "black", weight: 1 })
                            }).addTo(this.map);
                        }
                    });
                }
            },
            cleanMap() {
                if (this.geojsonLayer) {
                    this.map.removeLayer(this.geojsonLayer);
                    this.geojsonLayer = null;
                }
                if (this.routingControl) {
                    this.map.removeControl(this.routingControl);
                    this.routingControl = null;
                }
            },
            setStartPoint() {
                this.map.once('click', (e) => {
                    if (this.startPoint) {
                        this.map.removeLayer(this.startPoint);
                    }
                    this.startPoint = L.marker(e.latlng).addTo(this.map);
                });
            },
            setEndPoint() {
                this.map.once('click', (e) => {
                    if (this.endPoint) {
                        this.map.removeLayer(this.endPoint);
                    }
                    this.endPoint = L.marker(e.latlng).addTo(this.map);
                });
            },
            calculatePath() {
                if (this.startPoint && this.endPoint) {
                    if (this.routingControl) {
                        this.map.removeControl(this.routingControl);
                    }
                    this.routingControl = L.Routing.control({
                        waypoints: [
                            L.latLng(this.startPoint.getLatLng()),
                            L.latLng(this.endPoint.getLatLng())
                        ],
                        router: L.Routing.osrmv1({
                            serviceUrl: `https://router.project-osrm.org/route/v1`
                        }),
                        routeWhileDragging: true,
                        showAlternatives: true,
                        fitSelectedRoutes: true,
                        show: false
                    }).addTo(this.map);
                }
            },
            initListeners() {
                this.map.on('click', (e) => {
                    console.log("Map clicked at ", e.latlng); 
                });
            },
            showLocationDlg() { 
                var ele = document.getElementById("div_searchLocation");
                ele.style.visibility = "visible";
            },
            closeLocationDlg() { 
                var ele = document.getElementById("div_searchLocation");
                ele.style.visibility = "hidden";
            },
            setLocation() { 
                var map = this.$parent.$data.map;
                var ele = document.getElementById("txt_search_lng");
                var lon = ele.value;
                ele = document.getElementById("txt_search_lat");
                var lat = ele.value;
                map.flyTo([lat, lon]);
            },
            restore() {
                var map = this.$parent.$data.map;
                map.setView([53.8008, -1.5491], 13);
            },
            showLevelDlg() { 
                var ele = document.getElementById("div_levelLocation");
                ele.style.visibility = "visible";
            },
            closeLevelDlg() { 
                var ele = document.getElementById("div_levelLocation");
                ele.style.visibility = "hidden";
            },
            setMapLevel() { 
                var map = this.$parent.$data.map;
                var ele = document.getElementById("txt_level_lng");
                var zoomLevel = ele.value;
                map.setView(map.getCenter(), zoomLevel); 
            },
            showMapRange() { 
                var map = this.$parent.$data.map;
                var ex = map.getBounds();
                var ymin = ex._southWest.lat;
                var xmin = ex._southWest.lng;
                var ymax = ex._northEast.lat;
                var xmax = ex._northEast.lng;
                var str = "Latitude：" + ymin + "to" + ymax + "；Longitude：" + xmin + "to" + xmax;
                this.$alert(str, 'Current map extent', {
                    confirmButtonText: 'Confirm',
                    callback: (action) => {
                    },
                });
            },
            showMapPixel() {
                var map = this.$parent.$data.map;
                var mapSize = map.getSize();
                this.$alert(mapSize, 'Current map container pixel size', {
                    confirmButtonText: 'Confirm',
                    callback: (action) => {
                    },
                });
            },
            showMapInfo() {
                var map = this.$parent.$data.map;
                var center = "The current view center is：" + map.getCenter();
                var zoom = "The current zoom level is：" + map.getZoom();
                this.$alert(center + ", " + zoom, 'Current map basic information', {
                    confirmButtonText: 'Confirm',
                    callback: (action) => {
                    },
                });
            },
        }
    }
</script>

<style>
#road {
        position: absolute;
        bottom: 10px;
        left: 0;
        right: 0;
        margin-left: auto;
        margin-right: auto;
        z-index: 400;
        text-align: center;
}
.div_dialog {
    visibility: hidden;
    z-index: 400;
    position: absolute;
    left: 50%;
    transform: translate(-50%);
    top: 150px;
    background: rgba(35, 35, 35, 0.7);
    border-radius: 4px;
    font-size: 12pt;
    line-height: 20pt;
    margin: 0pt;
    padding: 0pt;
    color: white;
    border: 1px solid rgb(133, 133, 133);
    font-family: 'Times New Roman', Times, serif;
    box-shadow: rgb(11, 234, 235) 0px 0px 10px inset;
}

.div_dialog_header {
    width: 100%;
    height: 10%;
    text-align: center;
    background: rgba(25, 25, 25, 0.7);
    border-bottom: thin solid rgb(145, 145, 145);
    border-top-right-radius: 4px;
    border-top-left-radius: 4px;
}

.div_dialog_body {
    width: 100%;
    height: 90%;
    background-color: rgba(46, 87, 113, 0.6);
    text-align: center;
    overflow: hidden;
    border-bottom-right-radius: 4px;
    border-bottom-left-radius: 4px;
}

.div_dialog input {
    color: white;
    background-color: rgb(100, 100, 100);
    border: 1 solid rgb(25, 25, 25);
    line-height: 18px;
    margin-top: 15px;
    margin-bottom: 8px;
}

.div_dialog button {
    color: white;
    background: linear-gradient(to top, rgb(45, 45, 45), rgb(145, 145, 145));
    border: 1 solid rgb(25, 25, 25);
    border-radius: 4px;
    font-size: 12pt;
    margin-bottom: 8px;
}

.div_dialog img {

    float: right;
    margin-right: 6px;
    margin-top: 4px;
}

.div_dialog a {

    color: rgb(228, 222, 222);
    padding: 5px;
}

.div_dialog select {
    background-color: rgb(100, 100, 100);
    color: white;
    font-size: 12pt;
    padding: 5px;
}
</style>