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

function generate_table_row(header, query, tweet) {
    output_string = '<tr class = "results-table">';
    output_string += '<th>' + header + '</th>';
    output_string += '<td>' + tweet[query] + '</td>';
    output_string += '</tr>';
    return output_string;

}

function search_data_base() {
    let input = document.getElementById('user-query').value;
    let url = getAPIBaseURL() + '/search/input/' + input;

    fetch(url, { method: 'get' })

    .then((response) => response.json())

    .then(function(tweet_list) {
        table_body = '';
        table_length = tweet_list.length;
        if (table_length > 5) {
            table_length = 5;
        }
        for (let k = 0; k < table_length; k++) {
            tweet = tweet_list[k];
            table_body += "<li> <table style='width:100%' class = 'results-table'> <tr class = 'top-level-table-heading'> <th><a href='{{ url_for('follower_chart')}}'>Bot Account</a></th><td><a href='{{ url_for('follower_chart')}}'>" + tweet['author_name'] + "</a></td></tr>";

            table_body += generate_table_row('Content', 'content', tweet);
            table_body += generate_table_row('Followers', 'followers', tweet);
            table_body += generate_table_row('Following', 'followed', tweet);
            table_body += generate_table_row('Date Published', 'date', tweet);
            table_body += '</table></li>'
        }
        let list = document.getElementById('results-list');
        if (list) {
            list.innerHTML = table_body;
        }
    })

    .catch(function(error) {
        console.log(error);
    });

}