//Click events
$(window).on("click", generalWindowClickEvents);
$("#userDropdownTrigger").on("click", dropdownAnimation);
$("#categoriesDropdownBtn").on("click", categoriesDropdownAnimation);
$(".mobileMenuIcon").on("click", showMobileMenu);
$("#collapseMobileMenu").on("click", collapseMobileMenu);

//Partners slides
$(document).ready(function(){
	$('#partnersLightSlider').lightSlider({
	    item:5,
	    loop:false,
	    slideMove:1,
	    slideMargin: 20,
	    easing: 'cubic-bezier(0.25, 0, 0.25, 1)',
	    speed:600,
	    responsive : [
	        {
	            breakpoint:800,
	            settings: {
	                item:3,
	                slideMove:1,
	                slideMargin:6,
	              }
	        },
	        {
	            breakpoint:480,
	            settings: {
	                item:2,
	                slideMove:1
	              }
	        }
	    ]
	}); 
});

//Scroll events
$(window).scroll(scrollingPage);

//Functions
function dropdownAnimation(e){
	$(".userMenu").toggleClass("showMenuItems");

	// Close the dropdown menu if the user clicks outside of it
	window.onclick = function(event) {
	  if ((!event.target.matches('#userDropdownTrigger')) && (!event.target.matches('.fa-angle-down'))) {
	    var userMenu = document.getElementsByClassName("userMenu");
	    var i;
	    for (i = 0; i < userMenu.length; i++) {
	      var openDropdown = userMenu[i];
	      if (openDropdown.classList.contains('showMenuItems')) {
	        openDropdown.classList.remove('showMenuItems');
	      }
	    }
	  }
	}
}

function categoriesDropdownAnimation(e){
	$(".categoriesLinks").toggleClass("showCategoriesLinks");
}

function slideShow(){
	if($("#landingPage .slides.active").next().length >= 1){
		let activeSlide = $("#landingPage .slides.active");
		let activeCategoryName = $("#landingPage .slides.active .textDescription h6");
		let activeCategoryHead = $("#landingPage .slides.active .textDescription h1");
		let activeCategoryDesc = $("#landingPage .slides.active .textDescription h2");
		let activeCategoryBtn = $("#landingPage .slides.active .textDescription a");
		
		activeCategoryName.removeClass("activeCategoryName");
		activeCategoryHead.removeClass("activeCategoryHead");
		activeCategoryDesc.removeClass("activeCategoryDesc");
		activeCategoryBtn.removeClass("activeCategoryBtn");

		activeSlide.next().addClass("active");
		activeSlide.removeClass("active");	

		$("#landingPage .slides.active .textDescription h6").addClass("activeCategoryName");
		$("#landingPage .slides.active .textDescription h1").addClass("activeCategoryHead");
		$("#landingPage .slides.active .textDescription h2").addClass("activeCategoryDesc");
		$("#landingPage .slides.active .textDescription a").addClass("activeCategoryBtn");
	}else{
		$("#landingPage .slides.active .textDescription h6").removeClass("activeCategoryName");
		$("#landingPage .slides.active .textDescription h1").removeClass("activeCategoryHead");
		$("#landingPage .slides.active .textDescription h2").removeClass("activeCategoryDesc");
		$("#landingPage .slides.active .textDescription a").removeClass("activeCategoryBtn");
		
		$("#landingPage .slides").removeClass("active");
		//$("#landingPage .slides .textDescription h6").remove("activeCategoryName");
		$("#landingPage .slides").first().addClass("active");
		//console.log($("#landingPage .slides").first());
		$("#landingPage .slides.active .textDescription h6").addClass("activeCategoryName");
		$("#landingPage .slides.active .textDescription h1").addClass("activeCategoryHead");
		$("#landingPage .slides.active .textDescription h2").addClass("activeCategoryDesc");
		$("#landingPage .slides.active .textDescription a").addClass("activeCategoryBtn");
	}
}

function showMobileMenu(e){
	e.preventDefault();
	$("#mobileNavigationMenu").css("left","0px");
}

function collapseMobileMenu(e){
	e.preventDefault();
	$("#mobileNavigationMenu").css("left","-310px");
}

function scrollingPage(e){
	//Fix NavBar to top when scrolled over
	if($(this).scrollTop() > 180){
		$("#bottomNav").addClass("fixedNav");
	}else{
		$("#bottomNav").removeClass("fixedNav");
	}
}

function generalWindowClickEvents(e){
	if(!e.target.matches("#mobileNavigationMenu") && 
		!e.target.matches("#mobileNavigationMenu a") &&
		!e.target.matches(".mobileMenuIcon i")){
		$("#mobileNavigationMenu").css("left","-310px");
	}
}