window.onload = initialize;

function initialize() {
    search_data_base()
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
    let start_date = document.getElementById('tweet-filter-start').value;
    let end_date = document.getElementById('tweet-filter-end').value;
    let hide_original_tweets = document.getElementById('show-tweets').checked;
    let hide_retweets = document.getElementById('show-retweets').checked;
    var query = new Object();
    query.start_date = start_date;
    query.end_date = end_date;
    query.hide_original_tweets = hide_original_tweets;
    query.hide_retweets = hide_retweets;
    query_json_string = JSON.stringify(query);
    let url = getAPIBaseURL() + '/rankings/input/' + query_json_string;

    fetch(url, { method: 'get' })

    .then((response) => response.json())

    .then(function(user_list) {
        table_body = '';
        table_length = user_list.length;
        if (table_length > 10) {
            table_length = 10;
        }
        for (let k = 0; k < table_length; k++) {
            user = user_list[k];
            table_body += "<li> <table style='width:100%' class = 'results-table'> <tr class = 'top-level-table-heading'> <th><a href='{{ url_for('follower_chart')}}'>Bot Account</a></th><td><a href='{{ url_for('follower_chart')}}'>" + user['author_name'] + "</a></td></tr>";
            table_body += generate_table_row('Followers', 'sorting_data', user);

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