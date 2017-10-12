var info;
var server_url = 'http://localhost:8000';
var api_video_list_url = server_url + '/api?format=json';
var api_categary_list_url = server_url + '/api/category?format=json';
var api_home_list_url = server_url + '/api/home?format=json';
var api_year_list_url = server_url + '/api/year?format=json';
var sel_category_list = $("#category-list");
var sel_video_list = $("#video-list");
var sel_year_list = $("#year-list");


function render_category_list() {
    $.getJSON(api_categary_list_url, {}, function (result) {
        console.log(result);
        var html = template("category-list-template", {
            categories: result
        });
        sel_category_list.html(html);
        //add click function
        sel_category_list.find("> li").each(function () {
            $(this).click(click_category);
        })
    });
}

function render_video_list(category) {
    content = {
        'category' : category
    };
    $.getJSON(api_video_list_url, content, function (result) {
        console.log(result);
        var html = template("video-list-template", {
            videos: result.results,
            server_url: server_url
        });
        sel_video_list.html(html);
        //add click function
        // sel_category_list.find("> li").each(function () {
        //     $(this).click(click_category);
        // })
    });
}function render_home_list() {
    content = {
    };
    $.getJSON(api_home_list_url, content, function (result) {
        console.log("home");
        console.log(result);
        var html = template("home-list-template", {
            pre_categorys: result,
            server_url: server_url
        });
        sel_video_list.html(html);
        //add click function
        // sel_category_list.find("> li").each(function () {
        //     $(this).click(click_category);
        // })
    });
}
function render_year_list() {
    $.getJSON(api_year_list_url, {}, function (result) {
        console.log(result);
        var html = template("year-list-template", {
            years: result,
        });
        sel_year_list.html(html);
        //add click function
        // sel_category_list.find("> li").each(function () {
        //     $(this).click(click_category);
        // })
    });
}

// return the current category name
function get_current_category() {
    cur_ = sel_category_list.find(".active span");
    var cur_category_name;
    if (cur_.length === 0) {
        cur_category_name = "";
    } else {
        cur_category_name = cur_.html();
    }
    console.log(cur_category_name);
    return cur_category_name;
}
function click_category() {
    //add active class to current button
    sel_category_list.find(".active").removeClass("active");
    $(this).addClass("active");

    //render the video list
    var category = $(this).attr('name');
    render_video_list(category);
}
function click_year(obj) {
    year = $(obj).text();
    cur_path = window.location.pathname;
    search = window.location.search;
    if (cur_path === '/') {
        cur_path = '/list/'
    }
    if (cur_path.indexOf("/vod/") >= 0) {
        cur_path = '/list/'
    }
    if (search === "") {
        window.location.href = cur_path + "?year=" + year;
    } else {
        window.location.href = cur_path + search + "&year=" + year;
    }
}
function click_more(obj) {
    category = $(obj).attr("name");
    sel_category_list.find('[name="'+category+'"]').click();
}

//$("ul.pagination").children().map(function(){
//     console.log($(this).find("a").attr("href"));
// })
function click_pagination() {
    text = $(this).text();
    console.log(text);
}


$(function () {
    // auto open and close for year button
    $('li.dropdown').mouseover(function () {
        $(this).addClass('open');
    }).mouseout(function () {
        $(this).removeClass('open');
    });

    //add year param to paginator
    $("ul.pagination > li").each(function () {
        $(this).click(click_pagination);
        var page_btn = $(this).find("[href]");
        href = page_btn.attr("href");
        href += "&year=" + $("#m-pagination").attr("year");
        page_btn.attr("href", href);
    });

    num_pages = $("#m-pagination").attr("num_pages");
    for (var page = 1; page <= num_pages; page++) {
        var href = "?page=" + page + "&year=" + $("#m-pagination").attr("year");
        var item = '<li><a href="' + href + '">' + page + '</a></li>';
        $("#goto-menue").append(item);
    }

    render_category_list();
    // render_video_list();
    render_home_list();
    render_year_list();

});