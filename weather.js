export default {
    template:`
    <a class="weatherwidget-io" href="https://forecast7.com/en/2d4437d98/marsabit-county/" data-label_1="MARSABIT COUNTY" data-label_2="WEATHER" data-theme="original" >MARSABIT COUNTY WEATHER</a>`,
    
    data() {
    },
    methods: {
        get_weather(d,s,id){
            var js,fjs=d.getElementsByTagName(s)[0];
            if(!d.getElementById(id)){
                js=d.createElement(s);
                js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);
            }
        }
                // (document,'script','weatherwidget-io-js')
    },
    mounted() {
        this.get_weather(d,s,id)
    }
};