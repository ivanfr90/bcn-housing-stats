
function requestData(type, years, callback) {
	var params = '';

	if (!years.some(isNaN)) {
		var paramYears = `years=${years.join(',')}`;
		if (paramYears) {
			params = `?${paramYears}`;
		}
	};

	$.ajax({
		url: `${ENDPOINT_RESOURCE_DATA}/${type}${params}`,
		success: function(data) {
			callback(data);
		},
		cache: false
	});
}
