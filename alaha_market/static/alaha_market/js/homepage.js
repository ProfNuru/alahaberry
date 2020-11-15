//Landing page Slideshow
setInterval(slideShow, 3000);


$(document).ready(function() {
    $('#categoryLightSlider, #newArrivalsLightSlider').lightSlider({
        item:4,
        loop:false,
        slideMove:2,
        slideMargin: 20,
        easing: 'cubic-bezier(0.25, 0, 0.25, 1)',
        speed:600,
        responsive : [
            {
                breakpoint:800,
                settings: {
                    item:2,
                    slideMove:1,
                    slideMargin:6,
                  }
            },
            {
                breakpoint:480,
                settings: {
                    item:1,
                    slideMove:1
                  }
            }
        ]
    }); 
});


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

