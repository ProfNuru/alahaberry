$("document").ready(function(){
    //alert("Working")
	//Click Events
	load_site_data();
    get_all_items();
    load_shopping_cart();

    $("#user-nav-menu").on("click", open_user_menu);
    $("#close-user-menu-btn").on("click", close_user_menu);
	$(".shopping-cart-btn").on("click", show_cart);
	$(".close-cart-btn").on("click", hide_cart);
	$(".shopping-cart").on("click", function(e){
		if(e.target == this){
			hide_cart();
		}
    });
    $(".modal-add-to-cart-btn").on("click", modal_add_item_to_cart);
    $("#clear-cart-btn").on("click", clear_shopping_cart);
    $("#submit-order-btn").on("click", submit_order)
    $("#place_order_btn").on("click", place_order);
    $(".subscribe-newsletter button").on("click", subscribe);
});

function close_user_menu(e){
    e.preventDefault();
    $("#user-menu").hide('slow')
}

function open_user_menu(){
    $("#user-menu").show('slow');
}


function show_cart(){
	$(".shopping-cart").show("slow");
}


function hide_cart(){
	$(".shopping-cart").hide("slow");
}


function show_item_modal(e){
	if(e.target.outerHTML == $(".item-in-cart")[0].outerHTML){
        let item_id = $(e.target.nextElementSibling).val();
        var all_items = JSON.parse(localStorage.getItem('alahaberry_products'));
        for(var i=0; i<all_items.length; i++){
            if(all_items[i].pk == parseInt(item_id)){
                let cart = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
                if(item_in_cart(all_items[i].pk,cart)){
                    alert("Item already in cart");
                }else{
                    cart_item = all_items[i];
                    cart_item['qty'] = 1;
                    cart_item['amount'] = all_items[i].fields.product_price;
                    cart.push(all_items[i]);

                    localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(cart));
                    load_shopping_cart();
                    show_cart();
                }
            }
        }
	}else if(e.target.outerHTML == $(".buy-single-item")[0].outerHTML){
        let item_id = $(e.target.parentNode.nextElementSibling.nextElementSibling).val();
        var all_items = JSON.parse(localStorage.getItem('alahaberry_products'));
        for(var i=0; i<all_items.length; i++){
            if(all_items[i].pk == parseInt(item_id)){
                cart_item = all_items[i];
                cart_item['qty'] = 1;
                cart_item['amount'] = all_items[i].fields.product_price;
                let cart = [all_items[i]];

                localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(cart));
                load_shopping_cart();
                submit_order();
            }
        }
    }else{
		let item_id = e.currentTarget.children[e.currentTarget.children.length-1].value;
        var all_items = JSON.parse(localStorage.getItem('alahaberry_products'));
        for(var i=0; i<all_items.length; i++){
            if(all_items[i].pk == parseInt(item_id)){
                $(".modal-body .item-gallery .selected-img").html('<img class="item-thumbnails" src="media/'+
                    all_items[i].fields.product_thumbnail+'" class="img-fluid">');
                var images_html = "<img class='item-thumbnails' src='media/"+
                    all_items[i].fields.product_thumbnail+"'>";
                if(all_items[i].fields.product_image1.length > 0){
                    images_html += "<img class='item-thumbnails' src='media/"+
                    all_items[i].fields.product_image1+"'>";
                }
                if(all_items[i].fields.product_image2.length > 0){
                    images_html += "<img class='item-thumbnails' src='media/"+
                    all_items[i].fields.product_image2+"'>";
                }
                if(all_items[i].fields.product_image3.length > 0){
                    images_html += "<img class='item-thumbnails' src='media/"+
                    all_items[i].fields.product_image3+"'>";
                }
                $(".modal-body .item-gallery .other-img").html(images_html);
                $(".modal-body .item-description .item-title").text(all_items[i].fields.product_name);
                $(".modal-body .item-description .about-item").text(all_items[i].fields.product_desc);
                $(".modal-body .item-description .item-cost .value").text(all_items[i].fields.product_price);
                $("#item-to-add").val(all_items[i].pk);
            }
        }
        load_item_damages(item_id);
        load_item_colors(item_id);
        $("#showItemModal").modal('show');
        $(".other-img .item-thumbnails").on("click", select_image);
        $("#buy-item-from-modal").on("click", buy_item_from_modal)

        function select_image(e){
            $(e.target).addClass("img-fluid");
            clicked_img = e.target.outerHTML;
            $(".selected-img").html(clicked_img);
        }

        function buy_item_from_modal(){
            let item_id = $("#item-to-add").val();
            var all_items = JSON.parse(localStorage.getItem('alahaberry_products'));
            for(var i=0; i<all_items.length; i++){
                if(all_items[i].pk == parseInt(item_id)){
                    cart_item = all_items[i];
                    cart_item['qty'] = 1;
                    cart_item['amount'] = all_items[i].fields.product_price;
                    let cart = [all_items[i]];

                    localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(cart));
                    load_shopping_cart();
                    submit_order();
                }
            }
        }

        function load_item_damages(item_id){
            $.ajax({
                url: 'item_damages/',
                type: 'get',
                data: {'item_id':item_id},
                success: function(response){
                    item_conditions = JSON.parse(response);

                    if(item_conditions.length <= 0){
                        $("#conditions-list").html('<div class="alert alert-success" role="alert">'+
                            '<b>Item in Perfect Condition</b></div>');
                        return;
                    }
                    $("#conditions-list").html("");
                    for(var c=0; c <= item_conditions.length; c++){
                        if(item_conditions[c]){
                            $("#conditions-list").append('<li class="media">'+
                                '<img src="media/'+item_conditions[c].fields.image+
                                '" class="align-self-start mr-3" alt="Condition photo" style="max-width:250px">'+
                                '<div class="media-body">'+
                                '<p style="font-weight:bolder">'+item_conditions[c].fields.description+
                                '</p></div>'+
                                '</li><hr>');
                            }
                    }
                }
            });
        }

        function load_item_colors(item_id){
            $.ajax({
                url: 'item_colors/',
                type: 'get',
                data: {item_id:item_id},
                success:function(response){
                    item_colors = JSON.parse(response);

                    if(item_colors.length <= 0){
                        $("#colors_checkboxes").html("No colors or types for item");
                        return;
                    }
                    $("#colors_checkboxes").html('<h5>SELECT COLORS/TYPES</h5><div class="form-check">'+
                                        '<input class="form-check-input" type="radio"'+
                                        ' name="item_color" id="default" value="0" checked>'+
                                        '<label class="form-check-label" for="default">'+
                                        'Default</label></div>');
                    for(var e = 0; e <= item_colors.length; e++){
                        if(item_colors[e]){
                            $("#colors_checkboxes").append('<div class="form-check">'+
                                        '<input class="form-check-input" type="radio"'+
                                        ' name="item_color" id="color'+item_colors[e].pk.toString()+
                                        '" value="'+item_colors[e].pk.toString()+'">'+
                                        '<label class="form-check-label" for="color'+
                                        item_colors[e].pk.toString()+'">'+item_colors[e].fields.color+
                                        '</label></div>');
                        }
                    }
                    $('input[type=radio][name=item_color]').on('change', function() {
                      if($(this).val() == "0"){

                        for(var i=0; i<all_items.length; i++){
                            if(all_items[i].pk == parseInt(item_id)){
                                $(".modal-body .item-gallery .selected-img").html('<img class="item-thumbnails" src="media/'+
                                    all_items[i].fields.product_thumbnail+'" class="img-fluid">');
                                var image_html = "<img class='item-thumbnails' src='media/"+
                                    all_items[i].fields.product_thumbnail+"'>";
                                if(all_items[i].fields.product_image1.length > 0){
                                    image_html += "<img class='item-thumbnails' src='media/"+
                                    all_items[i].fields.product_image1+"'>";
                                }
                                if(all_items[i].fields.product_image2.length > 0){
                                    image_html += "<img class='item-thumbnails' src='media/"+
                                    all_items[i].fields.product_image2+"'>";
                                }
                                if(all_items[i].fields.product_image3.length > 0){
                                    image_html += "<img class='item-thumbnails' src='media/"+
                                    all_items[i].fields.product_image3+"'>";
                                }
                                $(".modal-body .item-gallery .other-img").html(image_html);
                                $(".other-img .item-thumbnails").on("click", select_image);
                            }
                        }
                      }else{
                        for(var f = 0; f <= item_colors.length; f++){
                            if(item_colors[f] && $(this).val() == item_colors[f].pk){
                                $(".modal-body .item-gallery .selected-img").html('<img class="item-thumbnails" src="media/'+
                                    item_colors[f].fields.image1+'" class="img-fluid">');
                                var colors_img = "<img class='item-thumbnails' src='media/"+
                                    item_colors[f].fields.image1+"'>";
                                if(item_colors[f].fields.image2.length > 0){
                                    colors_img += "<img class='item-thumbnails' src='media/"+
                                        item_colors[f].fields.image2+"'>";
                                }
                                if(item_colors[f].fields.image3.length > 0){
                                    colors_img += "<img class='item-thumbnails' src='media/"+
                                        item_colors[f].fields.image3+"'>";
                                }
                                if(item_colors[f].fields.image4.length > 0){
                                    colors_img += "<img class='item-thumbnails' src='media/"+
                                        item_colors[f].fields.image4+"'>";
                                }

                                $(".modal-body .item-gallery .other-img").html(colors_img);
                                $(".other-img .item-thumbnails").on("click", select_image);
                            }
                        }

                      }
                    });
                }
            });
        }
	}
}


function get_all_items(){
    // Check if search has been made
    var search_term = getUrlParameter("search-field");
    if(search_term == undefined){
        search_term = "";
    }else{
        search_term = search_term.replace("+"," ");
    }
    
    $.ajax({
        url: 'initialize_page/',
        type: 'get',
        success: function(response){
        	localStorage.setItem('alahaberry_products',response);
            let models = JSON.parse(response);
            
            for(var i=0; i<models.length; i++){
                if(search_term.length > 0){
                    if(!isNaN(search_term)){
                        if(search_term == models[i].fields.category.toString()){
                            if(models[i].fields.featured){
                                $(".popular-items .items").append('<div class="card"><img loading="lazy" src="media/'+ 
                                    models[i].fields.product_thumbnail +
                                    '" class="card-img-top" alt="Items image"><div class="card-body"><h6 class="item-name">' +
                                    models[i].fields.product_name+ 
                                    '</h6><p class="card-text">GHC <span class="item-price">'+ 
                                    models[i].fields.product_price +
                                    '</span></p><button class="buy-single-item btn btn-danger">BUY NOW</button></div><div class="item-in-cart"><i class="fas fa-shopping-cart"></i> ADD TO CART</div><input type="hidden" class="item_id" value="'+ models[i].pk +'"></div>');
                            }else{
                                $(".new-items .items").append('<div class="card"><img loading="lazy" src="media/'+ 
                                    models[i].fields.product_thumbnail +
                                    '" class="card-img-top" alt="Items image"><div class="card-body"><h6 class="item-name">'+
                                    models[i].fields.product_name+ 
                                    '</h6><p class="card-text">GHC <span class="item-price">'+ 
                                    models[i].fields.product_price +
                                    '</span></p><button class="buy-single-item btn btn-danger">BUY NOW</button></div><div class="item-in-cart"><i class="fas fa-shopping-cart"></i> ADD TO CART</div><input type="hidden" class="item_id" value="'+ models[i].pk +'"></div>');
                            }
                        }
                    }else if(models[i].fields.product_name.toLowerCase().includes(search_term.toLowerCase())){
                        if(models[i].fields.featured){
                            $(".popular-items .items").append('<div class="card"><img loading="lazy" src="media/'+ 
                                models[i].fields.product_thumbnail +
                                '" class="card-img-top" alt="Items image"><div class="card-body"><h6 class="item-name">' +
                                models[i].fields.product_name+ 
                                '</h6><p class="card-text">GHC <span class="item-price">'+ 
                                models[i].fields.product_price +
                                '</span></p><button class="buy-single-item btn btn-danger">BUY NOW</button></div><div class="item-in-cart"><i class="fas fa-shopping-cart"></i> ADD TO CART</div><input type="hidden" class="item_id" value="'+ models[i].pk +'"></div>');
                        }else{
                            $(".new-items .items").append('<div class="card"><img loading="lazy" src="media/'+ 
                                models[i].fields.product_thumbnail +
                                '" class="card-img-top" alt="Items image"><div class="card-body"><h6 class="item-name">'+
                                models[i].fields.product_name+ 
                                '</h6><p class="card-text">GHC <span class="item-price">'+ 
                                models[i].fields.product_price +
                                '</span></p><button class="buy-single-item btn btn-danger">BUY NOW</button></div><div class="item-in-cart"><i class="fas fa-shopping-cart"></i> ADD TO CART</div><input type="hidden" class="item_id" value="'+ models[i].pk +'"></div>');
                        }
                    }
                }else{
                    if(models[i].fields.featured){
                        $(".popular-items .items").append('<div class="card"><img loading="lazy" src="media/'+ 
                            models[i].fields.product_thumbnail +
                            '" class="card-img-top" alt="Items image"><div class="card-body"><h6 class="item-name">' +
                            models[i].fields.product_name+
                            '</h6><p class="card-text">GHC <span class="item-price">'+ 
                            models[i].fields.product_price +
                            '</span></p><button class="buy-single-item btn btn-danger">BUY NOW</button></div><div class="item-in-cart"><i class="fas fa-shopping-cart"></i> ADD TO CART</div><input type="hidden" class="item_id" value="'+ models[i].pk +'"></div>');
                    }else{
                        $(".new-items .items").append('<div class="card"><img loading="lazy" src="media/'+ 
                            models[i].fields.product_thumbnail +
                            '" class="card-img-top" alt="Items image"><div class="card-body"><h6 class="item-name">' +
                            models[i].fields.product_name+ 
                            '</h6><p class="card-text">GHC <span class="item-price">'+ 
                            models[i].fields.product_price +
                            '</span></p><button class="buy-single-item btn btn-danger">BUY NOW</button></div><div class="item-in-cart"><i class="fas fa-shopping-cart"></i> ADD TO CART</div><input type="hidden" class="item_id" value="'+ models[i].pk +'"></div>');
                    }
                }
            }
            if($(".popular-items .items").children().length <= 0 && $(".new-items .items").children().length <= 0){
                $(".popular-items").html("<h4 style='text-align:center;color:darkred;font-style:italic;'>No results for your search!</h4>");
                $(".products-heading").hide();
            }
			$(".card").on("click", show_item_modal);
        }
    });
}


function load_site_data(){
    $.ajax({
        url: 'site_data/',
        type: 'get',
        success: function(response){
            let site_data = JSON.parse(response);

            $("#favicon").attr("href","/media/"+site_data[site_data.length-1].favicon);
            $("header.landing-page").css("background-image","url(media/"+site_data[site_data.length-1].cover_photo+")");
            $(".landing-msg h3").html('<img src="media/' + site_data[site_data.length-1].logo + '">');
            $(".main-footer .about-shop .shop-image").html('<img src="media/' + site_data[site_data.length-1].logo + '" class="img-fluid">');
            $(".shop-description").html('<p>'+site_data[site_data.length-1].about+'</p>');
            $(".shop-address").html('<p>'+site_data[site_data.length-1].address+'</p>');
            $(".shop-contacts").html('<p>'+site_data[site_data.length-1].contact1+'</p>');

            //User menu icon
            $("#icon-on-menu img").attr("src", "/media/"+site_data[site_data.length-1].logo);
            
            //Social media links
            if(site_data[site_data.length-1].facebook_url){
                $(".shop-social-media").append("<a href='"+
                    site_data[site_data.length-1].facebook_url
                    +"'><i class='fab fa-facebook'></i></a>");
            }
            if(site_data[site_data.length-1].twitter_url){
                $(".shop-social-media").append("<a href='"+
                    site_data[site_data.length-1].twitter_url
                    +"'><i class='fab fa-twitter'></i></a>");
            }
            if(site_data[site_data.length-1].instagram_url){
                $(".shop-social-media").append("<a href='"+
                    site_data[site_data.length-1].instagram_url
                    +"'><i class='fab fa-instagram'></i></a>");
            }
            if(site_data[site_data.length-1].linkedin_url){
                $(".shop-social-media").append("<a href='"+
                    site_data[site_data.length-1].linkedin_url
                    +"'><i class='fab fa-linkedin'></i></a>");
            }
        }
    })
}


function load_shopping_cart(){
    if(localStorage.getItem('alahaberry_shopping_cart') === null){
        var cart = [];
        localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(cart));
        $("div.cart-notify").text(cart.length.toString());
        $("#cart-feedback").text("Cart is empty!")
    }else{
        var all_cart_items = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
        $(".shopping-cart .cart .cart-items tbody").html("");
        var grand_total = 0;
        for(var i=0; i<all_cart_items.length; i++){
            $(".shopping-cart .cart .cart-items tbody").append('<tr><td class="remove-item"><i class="fas fa-trash"></i>'+
                '<input type="hidden" value="'+ all_cart_items[i].pk+'">'+
                '</td><td class="item-img"><img src="media/'+
                all_cart_items[i].fields.product_thumbnail+'"></td><td class="item-desc"><h6 class="item-name">'+
                all_cart_items[i].fields.product_name+'</h6><h6 class="item-price">GHC '+
                all_cart_items[i].fields.product_price+'</h6></td><td class="item-qty"><input style="text-align:center" type="text" name="qty" class="cart-item-qty" value="'+
                all_cart_items[i].qty+'"></td><td class="item-amount">GHC <span>'+
                all_cart_items[i].fields.product_price+'</span></td></tr>');
                grand_total += parseFloat(all_cart_items[i].amount);
        }
        $("div.cart-notify").text(all_cart_items.length.toString());
        $("#cart-total").text("GHC "+grand_total.toFixed(2));
        $("#cart-feedback").text("Showing "+all_cart_items.length.toString()+" item(s)")
    }
    
    $(".remove-item i").on("click", remove_item_from_cart);
    $(".cart-item-qty").on("keyup", calculate_amounts);

    function remove_item_from_cart(e){
        let item_id = $(e.target.nextElementSibling).val();
        var cart = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
        
        let n_cart = [];
        for(var i=0; i<cart.length; i++){
            if(cart[i].pk != parseInt(item_id)){
                n_cart.push(cart[i]);
            }
        }
        localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(n_cart));
        load_shopping_cart();
    }

    function calculate_amounts(e){
        var new_qty = $(this).val();
        var item_row = $(this).parent().parent().children()[0];
        var item_id = $($(item_row).children()[1]).val();
        var cart = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
        var grand_total = 0;
        for(var i=0; i<cart.length; i++){
            if(cart[i].pk == parseInt(item_id)){
                if(isNaN(parseInt(new_qty))){
                    cart[i].qty = 1;
                    cart[i].amount = 1 * parseFloat(cart[i].fields.product_price);
                }else{
                    cart[i].qty = parseInt(new_qty);
                    cart[i].amount = parseInt(new_qty) * parseFloat(cart[i].fields.product_price);
                }
            }
            grand_total += parseFloat(cart[i].amount);
        }
        localStorage.setItem('alahaberry_shopping_cart',JSON.stringify(cart));
        $("#cart-total").text("GHC "+grand_total.toFixed(2));
    }
}


function item_in_cart(item_id,cart){
    for(var i=0; i<cart.length; i++){
        if(cart[i].pk == item_id){
            return true;
        }
    }
    return false;
}


function modal_add_item_to_cart(e){
    let item_id = $(e.target.nextElementSibling).val();
    var all_items = JSON.parse(localStorage.getItem('alahaberry_products'));
    for(var i=0; i<all_items.length; i++){
        if(all_items[i].pk == parseInt(item_id)){
            let cart = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
            
            if(item_in_cart(all_items[i].pk,cart)){
                alert("Item already in cart");
            }else{
                all_items[i].qty = 1;
                all_items[i].amount = all_items[i].fields.product_price;
                cart.push(all_items[i]);
                localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(cart));
                load_shopping_cart();
                show_cart();
                $("#showItemModal").modal('hide');
            }
        }
    }
}


function clear_shopping_cart(){
    var cart = [];
    localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(cart));
    load_shopping_cart();
}


function verify_cart_items(){
    var verified = true;
    var all_cart_items = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
    var all_products = JSON.parse(localStorage.getItem('alahaberry_products'));

    for(var i=0; i<all_cart_items.length; i++){
        if(!containsObject(all_cart_items[i],all_products)){
            verified = false;
        }
    }
    return verified;
}


function submit_order(){
    //Check if cart is empty
    var cart = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
    if(cart.length <= 0){
        $("#orderMessage").html('<div class="alert alert-danger" role="alert">Cart is empty!</div>');
        setTimeout(function(){ 
            $("#orderMessage").html('');
        }, 5000);
        return;
    }

    //Check if items match current items
    if(verify_cart_items()){
        var grand_total = 0;
        $("#list_of_ordered_items tbody").html("");
        for(var i=0; i<cart.length; i++){
            $("#list_of_ordered_items tbody").append('<tr><td>'+
            cart[i].fields.product_name+'</td><td>'+
            cart[i].fields.product_price+'</td><td>'+
            cart[i].qty+'</td><td>'+
            cart[i].amount+'</td></tr>');
            grand_total += parseFloat(cart[i].amount);
        }
        $("#order-total").text("GHC "+grand_total.toFixed(2));
        $("#placeOrderModal").modal("show");
    }
}


function place_order(e){
    e.preventDefault();
    var cust_email = $("#customer_email").val();
    var cust_phone = $("#customer_phone").val();
    var total_amount = $("#cart-total").text().replace('GHC ','');
    if(cust_email.trim() == "" & cust_phone.trim() == ""){
        $("#orderFormMessage").html('<div class="alert alert-danger" role="alert">Email or Phone number field is required!</div>')
        setTimeout(function(){ 
            $("#orderFormMessage").html('');
        }, 5000);
        return;
    }

    var prepared_data = {
        'csrfmiddlewaretoken': $("#order_form input").val(),
        'cust_email': cust_email,
        'cust_phone': cust_phone,
        'total_amount': total_amount,
        'order_items': localStorage.getItem('alahaberry_shopping_cart')
    }

    $.ajax({
        url: $("#order_form").attr('method'),
        type: $("#order_form").attr('action'),
        data: prepared_data,
        dataType: "json",
        success: function(data){
            var feedback = JSON.parse(data)
            if(feedback.order_placed){
                $("#orderSubmittedFeedbackModal .modal-body").html('<div class="alert alert-success" role="alert">Thank you for placing an order. We will contact you via email or phone number!</div>');
                clear_shopping_cart();
                $("#placeOrderModal").modal("hide");
                $("#orderSubmittedFeedbackModal").modal("show");
            }else{
                $("#orderSubmittedFeedbackModal .modal-body").html('<div class="alert alert-danger" role="alert">Failed to submit order!</div>');
                $("#orderSubmittedFeedbackModal").modal("show");
            }
        }
    });
}


function containsObject(obj, list) {
    var i;
    for (i = 0; i < list.length; i++) {
        if (list[i].fields.product_uid === obj.fields.product_uid) {
            return true;
        }
    }
    return false;
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


