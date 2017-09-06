

function click_year(obj){
	year=$(obj).text();
	cur_path=window.location.pathname;
	search = window.location.search;
	if(cur_path === '/'){
		cur_path = '/list/'
	}
	if(cur_path.indexOf("/vod/") >=0 ){
		cur_path = '/list/'
	}
	if(search === ""){
		window.location.href= cur_path+"?year="+year;
	}else {
		window.location.href= cur_path+search+"&year="+year;
	}
}
//$("ul.pagination").children().map(function(){
//     console.log($(this).find("a").attr("href"));
// })
function click_pagination() {
    text=$(this).text();
    console.log(text);
}


$(function(){
	// auto open and close for year button
	// $('li.dropdown').mouseover(function() {
     // 	$(this).addClass('open');
     // }).mouseout(function() {
     //    $(this).removeClass('open');
    // });

	//add year param to paginator
	$("ul.pagination > li").each(function () {
        $(this).click(click_pagination);
        var page_btn = $(this).find("[href]");
        href = page_btn.attr("href");
        href += "&year="+$("#m-pagination").attr("year");
        page_btn.attr("href",href);
    });

	num_pages = $("#m-pagination").attr("num_pages");
	for(var page=1; page <= num_pages;page++){
	    var href = "?page=" +page+"&year="+$("#m-pagination").attr("year");
	    var item = '<li><a href="' + href + '">'+page+'</a></li>';
        $("#goto-menue").append(item);
    }


});