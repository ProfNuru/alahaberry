let filterText = $("#filter-orders");
let filterPending = $("#filter-pending-orders");

$(".view-order-details").on("click", open_order_details);

filterText.on("keyup", function(){
	let rows = $(".orders-list-table tbody tr");
	for(var i=0; i<rows.length; i++){
		if(rows[i].innerText.toLowerCase().indexOf(filterText.val().toLowerCase()) <= -1){
			rows[i].style.display = "none";
		}else{
			rows[i].style.display = "table-row";
		}
	}
});


filterPending.on("keyup", function(){
	let rows = $(".new-orders-table tbody tr");
	for(var i=0; i<rows.length; i++){
		if(rows[i].innerText.toLowerCase().indexOf(filterPending.val().toLowerCase()) <= -1){
			rows[i].style.display = "none";
		}else{
			rows[i].style.display = "table-row";
		}
	}
});


function open_order_details(e){
	e.preventDefault();
	let order_id = $(this)[0].dataset['index'];

	$.ajax({
		url: 'get_order_details/',
		type: 'GET',
		data: {'order_id':order_id},
		success: function(response){
			let items = JSON.parse(response);

			$("#order-details-modal .modal-title").text("Items in Order " + order_id);
			$("#ordered-items-table tbody").html("");

			var total_amount = 0;
			for(var i=0; i<items.items_list.length; i++){
				total_amount += items.items_list[i].amount
				$("#ordered-items-table tbody").append("<tr>"+
					"<td><a href='/"+items.items_list[i].product_id+"/"+
					items.items_list[i].product_name
					+"/' target='_blank'>"+items.items_list[i].product_uid+"</a></td>"+
					"<td>"+items.items_list[i].qty_ordered+"</td>"+
					"<td>"+items.items_list[i].amount+"</td>"+
					"<td>"+items.items_list[i].sell_cost+"</td>"+
					"<td><a href='/dashboard/profile/"+items.items_list[i].seller+"/' target='_blank'>"+items.items_list[i].seller+"</a></td>"+
					+"</tr>");
			}
			
			if(items.delivered){
				$("#order-status").html("<div class='alert alert-warning'>Order delivered!</div>");
			}else{
				$("#order-status").html("<button id='make-delivery-btn' class='btn btn-outline-success btn-lg'>Make Delivery</button>");
			}

			$("#make-delivery-btn").on("click", function(){
				$.ajax({
					url: 'make_delivery/',
					type: 'GET',
					data: {'order_id':order_id},
					success: function(res){
						console.log(res);
						$("#order-details-modal").modal('hide');
						location.reload();
					}
				})
			});

			$("#order-details-modal .modal-body h5").text("Total Amount Ordered: "+total_amount.toString());
			$("#order-details-modal .modal-body div#buyer_details").html("<h5 style='color:#030;font-weight:bolder;margin-left:15px;'>E-mail: "+
							items.customer_email+"</h5><h5 style='color:#030;font-weight:bolder;margin-left:15px;'>Phone Number: "+
							items.customer_phone+"</h5>");
			$("#order-details-modal").modal('show');
		}
	});
}

