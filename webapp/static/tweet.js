window.onload = initialize;

function initialize() {
    search_data_base();
}

function getAPIBaseURL() {
    let baseURL = window.location.protocol +
        '//' + window.location.hostname +
        ':' + window.location.port +
        '/api';
    return baseURL;
}

function search_data_base() {
    let url = getAPIBaseURL() + '/random-tweet/';
    fetch(url, { method: 'get' })
    .then((response) => response.json())
    .then(function(tweet_list) {
        tweet = tweet_list[0]
        document.getElementById("tweet_name").innerHTML = tweet['author_name'];
        document.getElementById("tweet_username").innerHTML = tweet['author_name'];
        document.getElementById("tweet_message").innerHTML = tweet['content'];
        document.getElementById("tweet_date").innerHTML = tweet['date'];
        document.getElementById("followers").textContent = tweet['followers'];
        document.getElementById("follower-chart-link").href = "/follower_chart/"+tweet['author_name'];
    })
    .catch(function(error) {
        console.log(error);
    });
}