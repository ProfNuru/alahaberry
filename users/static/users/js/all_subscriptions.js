let filterField = document.getElementById("filter-subscriptions");
filterField.addEventListener('keyup', filterSubscriptions);




/***
**** Functions
***/
function filterSubscriptions(){
	let filterValue = this.value.toLowerCase();
	let rows = $(".subscriptions-table tbody tr");
	//console.log(rows);
	for(var i=0; i<rows.length; i++){
		if(rows[i].innerText.toLowerCase().indexOf(filterValue) <= -1){
			rows[i].style.display = "none";
		}else{
			rows[i].style.display = "table-row";
		}
	}	
}