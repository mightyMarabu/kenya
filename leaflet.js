export default {
    template: "<div></div>",
    // data: {
    //   lat: 0,
    //   lng: 0,
    // },    
    mounted() {
        this.map = L.map(this.$el);
        this.map.addEventListener("click", this.get_location)
        // this.get_location()
        

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
                layers: "whats_here",
                transparent: 'true',
                format: 'image/png',
            }),
        }

        var pointLayer = {

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

      test(){
        console.log('Am I a function?')
      },
      
      set_point(x, y){
        console.log(x,y)
        var new_point = L.marker([x,y]).addTo(this.map);
        console.log(new_point)
      },

      async get_location(e){
            // var lat = 0.0;
            // var lng = 0.0;
            var coord = e.latlng;
            var lat = coord.lat;
            var lng = coord.lng;
            console.log("You clicked the map at latitude: " + lat + " and longitude: " + lng);
            this.set_point(lat,lng)
            },
      test(){
        console.log("clicktest")
      }
     },
      
  }
  

  // this.map.on('click', function(e){
  //   var coord = e.latlng;
  //   lat = coord.lat;
  //   lng = coord.lng;
  //   console.log("You clicked the map at latitude: " + lat + " and longitude: " + lng);