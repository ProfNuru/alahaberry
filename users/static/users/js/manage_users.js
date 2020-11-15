//Filter table
let filterValue = document.getElementById("filter-sellers");
filterValue.addEventListener('keyup', filterSellers);


/*
**	Functions
*/
function filterSellers(){
	let filterValue = this.value.toLowerCase();
	let rows = $(".sellers-table tbody tr");
	
	for(var i=0; i<rows.length; i++){
		if(rows[i].innerText.toLowerCase().indexOf(filterValue) <= -1){
			rows[i].style.display = "none";
		}else{
			rows[i].style.display = "table-row";
		}
	}	
}
