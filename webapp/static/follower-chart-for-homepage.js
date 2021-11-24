// code lossely based on some broken code from sebaoka: https://stackoverflow.com/questions/55428160/wrong-label-value-is-displayed-on-point-hover-chart-js
var timeFormat = 'YYYY/MM/DD';

// We used a handwritten account name to guarantee an interesting chart to display.
// Displaying a random tweet here didn't make sense because some
// bot behavior doesn't graph well (outliers throw off scale)
// this way the first graph users see isn't unnecessarily confusing
function getAccountName() {
    return "ANDY_PUCHINSKYI";
}

function getAPIBaseURL() {
    let baseURL = window.location.protocol +
        '//' + window.location.hostname +
        ':' + window.location.port +
        '/api';
    return baseURL;
}

function getData() {
    let url = getAPIBaseURL() + '/follower-chart/input/' + getAccountName();
    
    fetch(url, { method: 'get' })
    .then((response) => response.json())
    .then(function(api_data) {
        var config = {
            type: 'bubble',
            data: {
                datasets: [{
                    label: getAccountName(), data: api_data,
                    fill: true, borderColor: "#c45850"}]},
            options: {
                responsive: true,
                title: { display: true, text: "Follower Count When Bot Tweets" },
                scales: {
                    xAxes: [{
                        type: "time",
                        time: {format: timeFormat,},
                        scaleLabel: {display: true, labelString: 'Date'}}],
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Number of Followers'}}]
        }}};
        return config;})
    .then(function(config) {
        var canvas_element = document.getElementById("follower-chart").getContext("2d");
        window.myLine = new Chart(canvas_element, config);})
    .catch(function(error) {
        console.log(error);});
};

window.onload = function() {
    getData();
};