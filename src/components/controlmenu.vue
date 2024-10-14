<template>
    <div id="menu">
        <el-button-group>
            <el-button type="info" v-for="item in items" :key="item" @click="btnClickEvt(item)">{{ item }}</el-button>
        </el-button-group>
    </div>
</template>

<script>
    import L from 'leaflet'
    import 'leaflet/dist/leaflet.css'
    import $ from 'jquery'

    export default {
        data() {
            return {
                items: ['Clear','Household deprivation','Dwelling Age Band Counts','Median House Prices','Method of travel to workplace','National Statistics Socio-economic Classification','Occupation'],  
                geojsonLayer: null,
                currentPopup: null,
                pendingPopupContent: null,
                pendingPopupLatLng: null
            };
        },
        mounted(){
            this.setupEventHandlers();
        },

        methods: {
            btnClickEvt(item) {
                var map = this.$parent.$data.map;
                this.clearMap();
                switch (item) {
                    case 'Household deprivation':
                        this.loadGeoJSON('household.geojson');
                        break;
                    case 'Dwelling Age Band Counts':
                        this.loadGeoJSON('housingage.geojson');
                        break;
                    case 'Median House Prices':
                        this.loadGeoJSON('median.geojson');
                        break;
                    case 'Method of travel to workplace':
                        this.loadGeoJSON('method.geojson');
                        break;
                    case 'National Statistics Socio-economic Classification':
                        this.loadGeoJSON('national.geojson');
                        break;
                    case 'Occupation':
                        this.loadGeoJSON('occupation.geojson');
                        break;
                    case 'Clear':
                        break;
                }
            },
            loadGeoJSON(filename) {
                var map = this.$parent.$data.map;
                const url = `${process.env.BASE_URL}static/data/${filename}?t=${new Date().getTime()}`;
                $.ajax({
                    url: url,
                    success: (result) => {
                        this.geojsonLayer = L.geoJSON(result, {
                            style: () => ({ color: "blue", weight: 1 }),
                            onEachFeature: (feature, layer) => {
                                layer.on('click', (e) => {
                                    this.showPopup(feature.properties, e.latlng);
                                });
                            }
                        }).addTo(map);
                    }
                });
            },
            clearMap() {
                var map = this.$parent.$data.map;
                if (this.geojsonLayer) {
                    map.removeLayer(this.geojsonLayer);
                    this.geojsonLayer = null;
                }
                if (this.currentPopup) {
                    map.closePopup(this.currentPopup);
                    this.currentPopup = null;
                }
            },
        
            showPopup(properties, latlng) {
                const map = this.$parent.$data.map;

                if (this.currentPopup) {
                    map.closePopup(this.currentPopup);
                    this.currentPopup = null;
                }
                const content = this.createPopupContent(properties);
                this.currentPopup = L.popup()
                    .setLatLng(latlng)
                    .setContent(content)
                    .openOn(map);
            },
            createPopupContent(properties) {
                let content = '<div><h4>Details</h4><ul>';
                Object.keys(properties).forEach(key => {
                    if (key !== 'label') {
                        content += `<li><strong>${key}:</strong> ${properties[key]}</li>`;
                    }
                });
                content += '</ul></div>';
                return content;
            },
            setupEventHandlers() {
                const map = this.$parent.$data.map;
                map.on('zoomstart movestart', () => {
                    if (this.currentPopup) {
                        this.pendingPopupContent = this.currentPopup.getContent();
                        this.pendingPopupLatLng = this.currentPopup.getLatLng();
                        map.closePopup(this.currentPopup);
                        this.currentPopup = null;
                    }
                });
                map.on('zoomend moveend', () => {
                    if (this.pendingPopupContent && this.pendingPopupLatLng) {
                        this.currentPopup = L.popup()
                            .setLatLng(this.pendingPopupLatLng)
                            .setContent(this.pendingPopupContent)
                            .openOn(map);
                        this.pendingPopupContent = null;
                        this.pendingPopupLatLng = null;
                    }
                });
            },            

        }
    }
</script>

<style>
    #menu {
        position: absolute;
        top: 80px;
        left: 0;
        right: 0;
        margin-left: auto;
        margin-right: auto;
        z-index: 400;
        text-align: center;
    }
</style>