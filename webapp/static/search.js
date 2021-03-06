window.onload = initialize;
var start_index = 0;
var end_index = 10;

var selected_order_bar = "descending"
var selected_sort_bar = "Followers"

function initialize() {
    assign_colors(selected_order_bar, selected_sort_bar)
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

function display_ascending() {
    if (selected_order_bar != "ascending") {
        start_index = 0;
        end_index = 10;
    }
    selected_order_bar = "ascending";
    assign_colors(selected_order_bar, selected_sort_bar);
}

function display_descending() {
    if (selected_order_bar != "descending") {
        start_index = 0
        end_index = 10
    }
    selected_order_bar = "descending";
    assign_colors(selected_order_bar, selected_sort_bar);
}

function display_followers() {
    selected_sort_bar = "Followers";
    assign_colors(selected_order_bar, selected_sort_bar);
}

function display_alphabetically() {
    selected_sort_bar = "Alphabetically";
    assign_colors(selected_order_bar, selected_sort_bar);
}

function display_following() {
    selected_sort_bar = "Following";
    assign_colors(selected_order_bar, selected_sort_bar);
}

// signals what filters have been selected
function assign_colors(selected_order_option, selected_sort_option) {
    let ascending_button = document.getElementById("ascending-order-button");
    let descending_button = document.getElementById("descending-order-button");

    let followers_button = document.getElementById("sort-by-followers-button");
    let alphabetically_button = document.getElementById("sort-alphabetically-button");
    let following_button = document.getElementById("sort-by-following-button");

    let selected_color = "Grey";
    let non_selected_color = "#f1f1f1";

    if (selected_order_option == "ascending") {
        ascending_button.style.backgroundColor = selected_color;
        descending_button.style.backgroundColor = non_selected_color;
    } else if (selected_order_option == "descending") {
        ascending_button.style.backgroundColor = non_selected_color;
        descending_button.style.backgroundColor = selected_color;
    }

    if (selected_sort_option == "Followers") {
        followers_button.style.backgroundColor = selected_color;
        alphabetically_button.style.backgroundColor = non_selected_color;
        following_button.style.backgroundColor = non_selected_color;
    } else if (selected_sort_option == "Alphabetically") {
        followers_button.style.backgroundColor = non_selected_color;
        alphabetically_button.style.backgroundColor = selected_color;
        following_button.style.backgroundColor = non_selected_color;
    } else if (selected_sort_option == "Following") {
        followers_button.style.backgroundColor = non_selected_color;
        alphabetically_button.style.backgroundColor = non_selected_color;
        following_button.style.backgroundColor = selected_color;
    }
}

function generate_table(tweet) {
    table_body = '';
    table_body += "<li> <table style='width:100%' class = 'results-table'> <tr class = 'top-level-table-heading'> <th><a>Bot Account</a></th><td><a href='/follower_chart/";
    table_body += tweet['author_name'];
    table_body += "'>" + tweet['author_name'] + "</a></td></tr>";
    table_body += generate_table_row('Content', 'content', tweet);
    table_body += generate_table_row('Followers', 'followers', tweet);
    table_body += generate_table_row('Following', 'followed', tweet);
    table_body += generate_table_row('Date Published', 'date', tweet);
    table_body += '</table></li>';
    return table_body;
}

function search_data_base() {
    let input = document.getElementById('user-query').value;

    let start_date = document.getElementById('tweet-filter-start').value;
    let end_date = document.getElementById('tweet-filter-end').value;

    let query = new Object();
    query.search_string = input;
    query.sort_metric = selected_sort_bar;
    query.start_date = start_date;
    query.end_date = end_date;

    query_json_string = JSON.stringify(query);
    let url = getAPIBaseURL() + '/search/input/' + query_json_string;
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function(user_list) {
            current_data = user_list;
            display_json(user_list, 0, 10);
        })
        .catch(function(error) {
            console.log(error);
        });
}

function iterate_results_forward() {
    start_index = end_index
    if (end_index + 10 < current_data.length) {
        end_index += 10;
    } else {
        end_index = current_data.length - 1;
    }
    display_json(current_data, start_index, end_index)
}

function iterate_results_back() {
    end_index = start_index;
    if (start_index - 10 >= 0) {
        start_index -= 10;
    } else {
        start_index = 0;
    }
    display_json(current_data, start_index, end_index)
}

function display_json(user_list, start_i, end_i) {
    let first_index = start_i;
    let final_index = end_i;

    let list_body = '';
    let table_length = user_list.length;
    if (final_index >= table_length) {
        final_index = table_length - 1;
    } else if (final_index < 0) {
        final_index = 0;
    }

    if (selected_order_bar == "descending") {
        interval = 1;
        for (let i = first_index; i < final_index; i++) {
            list_body += generate_table(user_list[i]);
        }
    } else {
        first_index = table_length - (start_i + 1);
        final_index = table_length - (end_i + 1);
        for (let i = first_index; i > final_index; i--) {
            list_body += generate_table(user_list[i]);
        }
    }

    let list = document.getElementById('results-list');

    if (list) {
        list.innerHTML = list_body;
    }
}