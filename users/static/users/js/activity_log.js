//Filter table
let filterValue = document.getElementById("filter-latest-activity");
filterValue.addEventListener('keyup', filterActivityLogs);


/*
**	Functions
*/
function filterActivityLogs(){
	let filterValue = this.value.toLowerCase();
	let rows = $(".new-orders-table tbody tr");
	
	for(var i=0; i<rows.length; i++){
		if(rows[i].innerText.toLowerCase().indexOf(filterValue) <= -1){
			rows[i].style.display = "none";
		}else{
			rows[i].style.display = "table-row";
		}
	}	
}
