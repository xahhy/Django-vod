
$(function(){
	// alert("init")
	$('li.dropdown').mouseover(function() {   
     	$(this).addClass('open');    
     }).mouseout(function() {
        $(this).removeClass('open');    
    }); 
});

function click_year(obj){
	year=$(obj).text();
	cur_path=window.location.pathname
	if(cur_path === '/'){
		cur_path = '/list/'
	}
	window.location.href= cur_path+"?year="+year;
}