let imgSelection = $(".selected-img");
$(".thumbnail").on("click", showSelectedImage);

$(document).ready(function() {
    $('#relatedItemLightSlider, #sameCategoryItemLightSlider').lightSlider({
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

//functions
function showSelectedImage(e){
	$(".thumbnail").removeClass("selected-thumb");
	$(this).addClass("selected-thumb");
	let selectedImage = $(this).html();
	imgSelection.html(selectedImage);
}