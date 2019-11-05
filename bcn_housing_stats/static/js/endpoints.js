function requestDataAverageRentalPrice(id, type) {
	$.ajax({
		url: `${ENDPOINT_RESOURCE_DATA}/${type}`, // ?years=2018
		success: function(data) {
			$.each(data.series, function(i, serie) {
				charts[id].addSeries({
					name: serie.year,
					data: serie.values
				}, false);
			});

			charts[id].xAxis[0].update({
				categories: data.categories
			}, true);

			charts[id].hideLoading();
		},
		cache: false
	});
}
