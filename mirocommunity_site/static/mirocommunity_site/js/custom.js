jQuery(document).ready(function(){
	
	$('.footer-nav li:last-child').css("background","none");
	$('#features ul li:last-child').css('margin-right','0px');
	$('.footer-nav li:first-child a').css('padding-left','0px');
	//this function attached focus and blur events with input elements
	var addFocusAndBlur = function($input, $val){
		
		$input.focus(function(){
			if (this.value == $val) {this.value = '';}
		});
		
		$input.blur(function(){
			if (this.value == '') {this.value = $val;}
		});
	}

	// example code to attach the events
	addFocusAndBlur(jQuery('#email'),'Your email goes here');


});


