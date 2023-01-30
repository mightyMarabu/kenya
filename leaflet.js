export default {
    template: "<div></div>",
    
    mounted() {
        this.map = L.map(this.$el);
    //   basemaps
        var basemaps = {
            OSM: L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png"),
            Google: L.tileLayer("http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",{
                maxZoom: 20,
                subdomains:['mt0','mt1','mt2','mt3']
            }),
        }
    //   geoserver
        var geoserver = 'http://141.51.249.91:8080/geoserver/marsabit/wms?'
        var overlay = { 
            NDVI_20220930: L.tileLayer.wms(geoserver, {
                layers: 'NDVI_20220930',
                transparent: 'true',
                format: 'image/png',
            }),
            what_is_here: L.tileLayer.wms(geoserver,{
                layers: "whats_this",
                transparent: 'true',
                format: 'image/png',
            }),
        }
    
    
  
        L.control.layers(basemaps, overlay).addTo(this.map);
    
        basemaps.OSM.addTo(this.map);
        overlay.what_is_here.addTo(this.map);

    },


    methods: {
      set_location(latitude, longitude) {
        this.target = L.latLng(latitude, longitude);
        this.map.setView(this.target, 9);
        if (this.marker) {
          this.map.removeLayer(this.marker);
        }
        this.marker = L.marker(this.target);
        this.marker.addTo(this.map);
      },
    },
  };
  