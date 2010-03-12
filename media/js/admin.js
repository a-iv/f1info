$().ready(function() {
//	$("select").not("td.team select,td.engine select,td.tyre select").sexyCombo();
	$("td.racer select").change(function() {
		var select = this;
		$.getJSON("/racer_last_info/" + select.value + "/", function(data) {
			var row = $(select).parent().parent();
			$("td.team select", row)[0].value = data.team;
			$("td.tyre select", row)[0].value = data.tyre;
			$("td.engine select", row)[0].value = data.engine;
		});		
	});
	
});