//Filter table
let filterValue = document.getElementById("filter-clerks");
filterValue.addEventListener('keyup', filterClerks);

/*
**	Functions
*/
function filterClerks(){
	let filterValue = this.value.toLowerCase();
	let rows = $(".clerks-table tbody tr");
	
	for(var i=0; i<rows.length; i++){
		if(rows[i].innerText.toLowerCase().indexOf(filterValue) <= -1){
			rows[i].style.display = "none";
		}else{
			rows[i].style.display = "table-row";
		}
	}	
}


