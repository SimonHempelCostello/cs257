window.onload = initialize;

function initialize() {

}

function getAPIBaseURL() {
    let baseURL = window.location.protocol +
        '//' + window.location.hostname +
        ':' + window.location.port +
        '/api';
    return baseURL;
}

function search_data_base() {
    let input = document.getElementById("user-query").value;
    let url = getAPIBaseURL() + "/search/input/" + input;

    fetch(url, { method: 'get' })

    .then((response) => response.json())

    .then(function(tweets) {
        let tableBody = '';
        for (let k = 0; k < tweets.length; k++) {
            a = k;
        }


    })

    .catch(function(error) {
        console.log(error);
    });

}