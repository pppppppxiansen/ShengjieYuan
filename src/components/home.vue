<template>
    <div id="app">
        <lf_map></lf_map>
        <top_bar></top_bar>
        <control_menu></control_menu>
        <road></road>
    </div>
</template>

<script>
import lf_map from './map.vue' 
import top_bar from './topbar.vue'
import control_menu from './controlmenu.vue'
import road from './road.vue'
export default {
    components: {
        lf_map,
        top_bar,
        control_menu,
        road
    },
    mounted(){
        document.title = 'Comprehensive map of Leeds';
    },

    data() {
        return {
            map: null,
        }
    }
};


</script>

<style>

</style>