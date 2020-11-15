let filterText = $("#filter-orders");
let filterPending = $("#filter-pending-orders");


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