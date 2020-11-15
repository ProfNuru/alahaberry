//Filter table
let filter = document.getElementById("filter-items");
filter.addEventListener('keyup', filterItems);

/*
**	Functions
*/
function filterItems(){
	let filterValue = this.value.toLowerCase();
	let rows = $(".items-table tbody tr");
	//console.log(rows);
	for(var i=0; i<rows.length; i++){
		if(rows[i].innerText.toLowerCase().indexOf(filterValue) <= -1){
			rows[i].style.display = "none";
		}else{
			rows[i].style.display = "table-row";
		}
	}	
}
