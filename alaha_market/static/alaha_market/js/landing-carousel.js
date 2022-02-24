// Populars items slider 1
console.log("Loading landing carousel");
new Glide('.glide', {
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
