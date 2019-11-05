
function requestDataAverageRentalPrice(id, type, callback) {
	$.ajax({
		url: `${ENDPOINT_RESOURCE_DATA}/${type}`, // ?years=2018
		success: function(data) {
			callback(id, data);
		},
		cache: false
	});
}
