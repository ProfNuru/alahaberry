//Filter table
let filterProducts = document.getElementById("filter-items");
let filterCategories = document.getElementById("filter-categories");
let filterLatestLogs = document.getElementById("filter-latest-items");


filterProducts.addEventListener('keyup', filterItems);
filterCategories.addEventListener('keyup', filterCategoryEntry);


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


function filterCategoryEntry(){
	let filterValue = this.value.toLowerCase();
	let rows = $(".categories-table tbody tr");

	for(var i=0; i<rows.length; i++){
		console.log(rows[i].innerText);
		if(rows[i].innerText.toLowerCase().indexOf(filterValue) <= -1){
			rows[i].style.display = "none";
		}else{
			rows[i].style.display = "table-row";
		}
	}
}