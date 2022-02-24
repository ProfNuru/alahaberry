$(".product-container .product-thumbs img").on("click", select_image);
$(".edit-qty .minus").on("click", decreaseProductQty);
$(".edit-qty .add").on("click", increaseProductQty);
$("#add-to-cart-btn").on("click", addToCart);
$("#buy-now-btn").on("click", buySingleItem);


function select_image(e){
	//console.log(e.currentTarget.src);
	$(".product-container .selected-img").html('<img src="'+e.currentTarget.src+'">');
}

function increaseProductQty(){
	let currentQty = parseInt($(this).prev().text());
	let newQty = currentQty + 1;
	let selected_qty = $(this).prev().html("<span>"+newQty+"</span>");
}

function decreaseProductQty(){
  let currentQty = parseInt($(this).next().text());
  if(currentQty > 1){
    let newQty = currentQty - 1;
    let selected_qty = $(this).next().html("<span>"+newQty+"</span>");
  }  
}


function addToCart(e){
	e.preventDefault();
	let item_id = $("#p_id").val();
	let item_qty = $(".edit-qty .qty-value").text();

	var all_items = JSON.parse(localStorage.getItem('alahaberry_products'));
	var all_cart_items = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));

	for(var i=0; i<all_items.length; i++){
		if(all_items.length > 0 && all_items[i].pk === parseInt(item_id)){
			for(j=0; j<all_cart_items.length; j++){
				if(all_items.length > 0 && all_cart_items[j].selected_item.pk === parseInt(item_id)){
					alert("Item already in cart");
					$("#shopping-cart").show();
					return;
				}
			}

			var item_in_cart = {
				'selected_item': all_items[i],
				'qty': parseInt(item_qty)
			};

			all_cart_items.push(item_in_cart);
			localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(all_cart_items));
			loadCart();
			$("#shopping-cart").show();
			return
		}
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

function buySingleItem(e){
	e.preventDefault();
	let item_id = $("#p_id").val();
	let item_qty = $(".edit-qty .qty-value").text();

	//Clear cart
	var cart = [];
    localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(cart));
	var all_cart_items = JSON.parse(localStorage.getItem('alahaberry_shopping_cart'));
	var all_items = JSON.parse(localStorage.getItem('alahaberry_products'));
	for(var i=0; i<all_items.length; i++){
		if(all_items.length > 0 && all_items[i].pk === parseInt(item_id)){
			let item_amt = parseFloat(all_items[i].fields.product_price)*parseInt(item_qty);
			$("#list_of_ordered_items").html('<div class="ordered-items">'+
              '<div class="item-img-and-name">'+
                '<img src="/media/'+all_items[i].fields.product_thumbnail+
                '" alt="Item image" class="me-3" style="width: 60px; height: 60px;" />'+
                '<h5>'+all_items[i].fields.product_name+'</h5>'+
              '</div>'+
              '<div class="item-price-and-qty">'+
                '<h6>GHS <span>'+parseFloat(all_items[i].fields.product_price).toFixed(2)+'</span></h6>'+
                '<h6>Qty: <span>'+item_qty+'</span></h6>'+
              '</div>'+
              '<div class="item-total-amount">'+
                '<h5>Amount: GHS <span>'+item_amt.toFixed(2)+'</span></h5>'+
              '</div></div><hr>');
			$(".item-totals-div h1 span").text(item_amt.toFixed(2));

			//Add to cart
			var item_in_cart = {
				'selected_item': all_items[i],
				'qty': parseInt(item_qty)
			};

			all_cart_items.push(item_in_cart);
			localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(all_cart_items));
			loadCart();
			break;
		}
	}

	$("#buySingleItemModal").modal("show");
}


function clearCart(){
    var cart = [];
    localStorage.setItem('alahaberry_shopping_cart', JSON.stringify(cart));
    loadCart();
}