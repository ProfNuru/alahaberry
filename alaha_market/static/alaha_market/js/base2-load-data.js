$("#shopping-cart").hide();
$("document").ready(function(){
    get_all_items();
    loadCart();
    track_searches();
    load_searches();
    
    $("#page-loader").fadeOut(1000);
    $("#clear-cart-btn").on("click", clearCart);
    $("#checkout-btn").on("click", checkoutFromCart);
    $("#place-order-btn").on("click", placeOrder);
    $("#subscribe-btn").on("click", subscribe);
    $("#search-cart-container .cart-div .cart-btn, #cart-btn, #shopping-cart .cart-header .close-cart").on("click",toggleCart);
});


function get_all_items(){
    console.log("Making AJAX request for all items");
    $.ajax({
        url: '/initialize_page/',
        type: 'get',
        success: function(response){
            localStorage.setItem('alahaberry_products',response);
            console.log("Request succeeded",response);
            // let product_models = JSON.parse(response);
            // console.log(product_models);
        },
        error:function(err){
            console.log("An error occurred:",err);
        }
    });
}


function getUrlParameter(name) {
    var urlOld          = window.location.href.split('?');
    urlOld[1]           = urlOld[1] || '';
    var urlBase         = urlOld[0];
    var urlQuery        = urlOld[1].split('#');
    urlQuery[1]         = urlQuery[1] || '';
    var parametersString = urlQuery[0].split('&');
    if (parametersString.length === 1 && parametersString[0] === '') {
        parametersString = [];
    }
    // console.log(parametersString);
    var anchor          = urlQuery[1] || '';

    var urlParameters = {};
    jQuery.each(parametersString, function (idx, parameterString) {
        paramName   = parameterString.split('=')[0];
        paramValue  = parameterString.split('=')[1];
        urlParameters[paramName] = paramValue;
    });
    return urlParameters[name];
}


function track_searches(){
    var search_term = getUrlParameter('search-field');
    if(search_term != undefined && search_term.length > 0){
        search_term = search_term.trim();
        search_term = search_term.replace(/\+/g,' ');
        search_term = search_term.replace(/%20/g,' ');
        if(localStorage.getItem('alahaberry_searches') === null){
            var searches = [search_term];
            localStorage.setItem('alahaberry_searches', JSON.stringify(searches));
        }else{
            var all_searches = JSON.parse(localStorage.getItem('alahaberry_searches'));
            if(!all_searches.includes(search_term)){
                all_searches.unshift(search_term);
            }
            if(all_searches.length > 6){
                all_searches.pop();
            }
            localStorage.setItem('alahaberry_searches', JSON.stringify(all_searches));
        }
    }
}


function load_searches(){
    var all_searches = JSON.parse(localStorage.getItem('alahaberry_searches'));
    if(all_searches == undefined){
        all_searches = [];
    }
    for(var i=0; i<all_searches.length; i++){
        $("#search-cart-container .search-div").append('<a href="/?search-field='+all_searches[i]+'" style="text-decoration:none" class="popular-searches">'+all_searches[i]+'</a>');
    }
}

function loadCart(){
    if(localStorage.getItem('alahaberry_shopping_cart') === null){
        var cart = [];
        localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(cart));
        $(".number-of-cart-items").text(cart.length.toString());
        $("#cart-feedback").text("Cart is empty!");
    }else{
        var all_cart_items = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
        $(".number-of-cart-items").text(all_cart_items.length.toString());
        if(all_cart_items <= 0){
            $("#cart-feedback").text("Cart is empty!");
        }
        $("#shopping-cart .cart-items").html("");
        var grand_total = 0;
        for(var i=0; i<all_cart_items.length; i++){
            let item_amount = parseFloat(all_cart_items[i].selected_item.fields.product_price) * all_cart_items[i].qty;
            grand_total += item_amount;
            $("#shopping-cart .cart-items").append('<div class="cart-item box-shadow"><span class="remove-item"><i class="fas fa-minus-circle"></i></span><div class="item-thumb">'+
                                                    '<img src="/media/'+all_cart_items[i].selected_item.fields.product_thumbnail+'">'+
                                                  '</div>'+
                                                  '<div class="item-name-price">'+
                                                    '<div class="item-name">'+all_cart_items[i].selected_item.fields.product_name+'</div>'+
                                                    '<div class="item-price">'+
                                                      '<span class="item-currency">GHS</span>'+
                                                      '<span class="price-value">'+all_cart_items[i].selected_item.fields.product_price+'</span>'+
                                                    '</div>'+
                                                  '</div>'+
                                                  '<div class="item-qty-control">'+
                                                    '<span class="increase"><i class="fas fa-plus"></i></span>'+
                                                    '<div class="selected-qty">'+all_cart_items[i].qty+'</div>'+
                                                    '<span class="decrease"><i class="fas fa-minus"></i></span>'+
                                                  '</div><input type="hidden" value="'+
                                                  +all_cart_items[i].selected_item.pk+'">'+
                                                '</div>');

        }
        $("#total-amount-of-items").text(grand_total.toFixed(2));
    }

    $("#shopping-cart .cart-item .item-qty-control .increase").on("click", increaseQty);
    $("#shopping-cart .cart-item .item-qty-control .decrease").on("click", decreaseQty);
    $("#shopping-cart .cart-item .remove-item").on("click", deleteItemFromCart);

    function increaseQty(e){
      let currentQty = parseInt($(this).next().text());
      let newQty = currentQty + 1;
      let selected_qty = $(this).next().text(newQty);

      //Update Quantity in cart
      let current_item_id = parseInt($(this).parent().next().val());
      var all_cart_items = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
      for(var k=0; k<all_cart_items.length; k++){
        if(all_cart_items[k].selected_item.pk == current_item_id){
            all_cart_items[k].qty = newQty;
        }
      }
      localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(all_cart_items));
      loadCart();
    }

    function decreaseQty(e){
      let currentQty = parseInt($(this).prev().text());
      if(currentQty > 1){
        let newQty = currentQty - 1;
        let selected_qty = $(this).prev().text(newQty);

        //Update Quantity in cart
        let current_item_id = parseInt($(this).parent().next().val());
        var all_cart_items = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
        for(var k=0; k<all_cart_items.length; k++){
           if(all_cart_items[k].selected_item.pk == current_item_id){
                all_cart_items[k].qty = newQty;
            }
        }
        localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(all_cart_items));
        loadCart();
      }  
    }

    function deleteItemFromCart(e){
        let item_id = $(this).parent().children().last().val();
        let all_cart_items = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
        let new_cart = [];
        for(var k=0; k<all_cart_items.length; k++){
            if(all_cart_items[k].selected_item.pk == parseInt(item_id)){
                console.log("item found", item_id, all_cart_items[k].selected_item.pk);
                continue;
            }else{
                new_cart.push(all_cart_items[k]);
            }
        }
        localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(new_cart));
        loadCart();
    }
}

function clearCart(){
    var cart = [];
    localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(cart));
    loadCart();
}


function checkoutFromCart(){
    let all_cart_items = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));

    if(all_cart_items.length > 0){
        $("#list_of_ordered_items").html('');
        let total_checkout_amount = 0
        for(var i=0; i<all_cart_items.length; i++){
            let item_amt = parseFloat(all_cart_items[i].selected_item.fields.product_price)*parseInt(all_cart_items[i].qty);
            total_checkout_amount += item_amt;
            $("#list_of_ordered_items").append('<div class="ordered-items">'+
              '<div class="item-img-and-name">'+
                '<img src="/media/'+all_cart_items[i].selected_item.fields.product_thumbnail+
                '" alt="Item image" class="me-3" style="width: 60px; height: 60px;" />'+
                '<h5>'+all_cart_items[i].selected_item.fields.product_name+'</h5>'+
              '</div>'+
              '<div class="item-price-and-qty">'+
                '<h6>GHS <span>'+parseFloat(all_cart_items[i].selected_item.fields.product_price).toFixed(2)+'</span></h6>'+
                '<h6>Qty: <span>'+all_cart_items[i].qty+'</span></h6>'+
              '</div>'+
              '<div class="item-total-amount">'+
                '<h5>Amount: GHS <span>'+item_amt.toFixed(2)+'</span></h5>'+
              '</div></div><hr>');
        }
        $(".item-totals-div h1 span").text(total_checkout_amount.toFixed(2));
        $("#buySingleItemModal").modal("show");
    }else{
        $("#cart-feedback").text("Add items to cart, then checkout!");
    }

}


function placeOrder(e){
    e.preventDefault();
    var cust_email = $("#customer_email").val();
    var cust_phone = $("#customer_phone").val();
    var total_amount = $(".item-totals-div h1 span").text();
    if(cust_email.trim() == "" & cust_phone.trim() == ""){
        $("#buySingleItemMessage").html('<div class="alert alert-danger" role="alert">Email or Phone number field is required!</div>')
        setTimeout(function(){ 
            $("#buySingleItemMessage").html('');
        }, 5000);
        return;
    }

    var prepared_data = {
        'csrfmiddlewaretoken': $("#order_form>input").val(),
        'cust_email': cust_email,
        'cust_phone': cust_phone,
        'total_amount': total_amount,
        'order_items': localStorage.getItem('alahaberry_shopping_cart')
    }

    $.ajax({
        url: $("#order_form").attr('action'),
        type: $("#order_form").attr('method'),
        data: prepared_data,
        dataType: "json",
        success: function(data){
            console.log(data);
            var feedback = JSON.parse(data)
            if(feedback.order_placed){
                $("#cart-feedback").html('<div class="alert alert-success" role="alert">Thank you for placing an order. We will contact you via email or phone number!</div>');
                clearCart();
                $("#list_of_ordered_items").html('');
                $("#buySingleItemModal").modal("hide");
                $("#shopping-cart").show();
            }else{
                $("#cart-feedback").html('<div class="alert alert-danger" role="alert">Failed to submit order!</div>');
                $("#shopping-cart").show();
            }
        }
    });
}


function subscribe(e){
    e.preventDefault();
    var sub_email = $("#subscription-email").val();
    if(sub_email.trim() == ""){
        alert("You must enter email field");
        return;
    }
    $.ajax({
        url: $("#subscribe-form").attr('action'),
        type: $("#subscribe-form").attr('method'),
        data: {'csrfmiddlewaretoken': $("#subscribe-form input:hidden").val(),
        'subscription_email': sub_email},
        dataType: 'json',
        success: function(data){
            sub_feedback = JSON.parse(data)
            if(sub_feedback.subscribed){
                alert("Subscribed successfully!");
            }
        }
    });
}


function toggleCart(){
  $("#shopping-cart").toggle("");
}

//Featured items slider 1
// new Glide('.featured-glide-1', {
//   type: 'carousel',
//   startAt: 0,
//   perView: 6,
//   perTouch: 1,
//   autoplay: 5000,
//   breakpoints: {
//     1200: {
//       perView: 4
//     },
//     800: {
//       perView: 3
//     },
//     420: {
//       perView: 2
//     },
//     280: {
//       perView: 1
//     }
//   }
// }).mount();

//Featured items slider 2
// new Glide('.featured-glide-2', {
//   type: 'carousel',
//   startAt: 0,
//   perView: 6,
//   perTouch: 1,
//   autoplay: 5000,
//   breakpoints: {
//     1200: {
//       perView: 4
//     },
//     800: {
//       perView: 3
//     },
//     420: {
//       perView: 2
//     },
//     280: {
//       perView: 1
//     }
//   }
// }).mount();

//Related items slider 1
// new Glide('.related-category-glide-1', {
//   type: 'carousel',
//   startAt: 0,
//   perView: 6,
//   perTouch: 1,
//   autoplay: 5000,
//   breakpoints: {
//     1200: {
//       perView: 4
//     },
//     800: {
//       perView: 3
//     },
//     420: {
//       perView: 2
//     },
//     280: {
//       perView: 1
//     }
//   }
// }).mount();
