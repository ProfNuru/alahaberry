$("document").ready(function(){
  // After successful loading
  //$("#page-loader").fadeOut(1000);
  $("#search-cart-container .cart-div .cart-btn, #cart-btn, #shopping-cart .cart-header .close-cart").on("click",toggleCart);
});

//Featured items slider 1
new Glide('.featured-glide-1', {
  type: 'carousel',
  startAt: 0,
  perView: 6,
  perTouch: 1,
  autoplay: 5000,
  breakpoints: {
    1200: {
      perView: 4
    },
    800: {
      perView: 3
    },
    420: {
      perView: 2
    },
    280: {
      perView: 1
    }
  }
}).mount();

//Featured items slider 2
new Glide('.featured-glide-2', {
  type: 'carousel',
  startAt: 0,
  perView: 6,
  perTouch: 1,
  autoplay: 5000,
  breakpoints: {
    1200: {
      perView: 4
    },
    800: {
      perView: 3
    },
    420: {
      perView: 2
    },
    280: {
      perView: 1
    }
  }
}).mount();

//Related items slider 1
new Glide('.related-category-glide-1', {
  type: 'carousel',
  startAt: 0,
  perView: 6,
  perTouch: 1,
  autoplay: 5000,
  breakpoints: {
    1200: {
      perView: 4
    },
    800: {
      perView: 3
    },
    420: {
      perView: 2
    },
    280: {
      perView: 1
    }
  }
}).mount();

//Featured items slider 2
new Glide('.related-category-glide-2', {
  type: 'carousel',
  startAt: 0,
  perView: 6,
  perTouch: 1,
  autoplay: 5000,
  breakpoints: {
    1200: {
      perView: 4
    },
    800: {
      perView: 3
    },
    420: {
      perView: 2
    },
    280: {
      perView: 1
    }
  }
}).mount();


function toggleCart(){
  $("#shopping-cart").toggle("");
}
