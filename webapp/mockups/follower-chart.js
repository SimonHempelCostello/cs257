// code lossely based on some broken code from sebaoka: https://embed.plnkr.co/JOI1fpgWIS0lvTeLUxUp/
var timeFormat = 'MM/DD/YYYY';
var config = {
    type: 'line',
    data: {
        datasets:[{
            label: "AUSTINLOVESBEER",
            data: [{x:"4/3/2015", y:45}, {x:"6/25/2015", y:48}, {x:"8/30/2015", y:52}, {x:"11/26/2015", y:70},  {x:"3/31/2018", y:65}, {x:"7/8/2018", y:41}, ],
            fill: true, borderColor: "#c45850"}]},
        options: {
            responsive: true,
            title:{display: true, text:"Follower Count When Bot Tweets"},
            scales:{
                xAxes: [{
                    type: "time",
                    time: {
                        format: timeFormat,
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Number of Followers'
                    }
                }],
                yAxes: [{
                    scaleLabel:{
                        display: true,
                        labelString: 'Date'
                    }
                }]
            }
        }
    };

    window.onload = function(){
        var canvas_element = document.getElementById("follower-chart").getContext("2d");
        window.myLine = new Chart(canvas_element, config);
    };

