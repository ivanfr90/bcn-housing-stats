
$(document).ready(function() {
	$("#btn-simple-data").click(function () {
		loadAndRender();
	});

	$('#collapse-historic-data').on('shown.bs.collapse', function () {
		typeSelected = HISTORIC_DATA;
	});

	$('#collapse-historic-data').on('hidden.bs.collapse', function () {
		typeSelected = null;
	});

	$('#collapse-simple-data').on('shown.bs.collapse', function () {
		typeSelected = SIMPLE_DATA;
	});

	$('#collapse-simple-data').on('hidden.bs.collapse', function () {
		typeSelected = null;
	});
});
