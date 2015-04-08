

$.fn.stars = function() {
    return this.each(function(i,e){$(e).html($('<span/>').width($(e).text()*16));});

};

$('.stars').stars();

$(document).ready(function(){

  $('#example').dataTable();





});


$(document).ready(function(){
	var str=location.href.toLowerCase();
	$(".nav li a").each(function() {
	if (str.indexOf(this.href.toLowerCase()) > -1) {
	$("li.active").removeClass("active");
	$(this).parent().addClass("active");
}
});

$("li.active").parents().each(function(){
if ($(this).is("li")){
$(this).addClass("active");
}
});
})