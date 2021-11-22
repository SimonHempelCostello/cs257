// code lossely based on some broken code from sebaoka: https://stackoverflow.com/questions/55428160/wrong-label-value-is-displayed-on-point-hover-chart-js
var timeFormat = 'YYYY/MM/DD';

//example is nytimes (as in @nytimes)
function getAccountName() {
    let accountName = window.location.pathname
    return accountName.substr("/follower_chart/".length);
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
    .then(function(data2) {
        console.log(data2);
        var config = {
            type: 'bubble',
            data: {
                datasets: [{
                    label: getAccountName(),
                    data: data2,
                    fill: true,
                    borderColor: "#c45850"}]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                title: { display: true, text: "Follower Count When Bot Tweets" },
                scales: {
                    xAxes: [{
                        type: "time",
                        time: {
                            format: timeFormat,},
                        scaleLabel: {
                            display: true,
                            labelString: 'Date'}}],
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Number of Followers'}}]
        }}};
        return config;})
    .then(function(config) {
        console.log(config);
        var canvas_element = document.getElementById("follower-chart").getContext("2d");
        window.myLine = new Chart(canvas_element, config);})
    .catch(function(error) {
        console.log(error);});
};


window.onload = function() {
    document.getElementById("title").innerHTML = getAccountName();
    getData();
};