function updateChartsTypeColumn(id, data) {
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
}

function updateCardDeck(id, data) {

	try {
		$.each(data.average_per_years, function(i, value) {
			$('#' + id).append(
				$('<div/>', {
					"class": 'card-text font-weight-bold',
					text: `${parseFloat(value.avg).toFixed(2)} euros (${value.year})`
				})
			);
		});
	} catch (e) {
		$('#' + id).append($('<p/>', {text: `${ERROR_LOADING_DATA}`}));
	}
}

var charts = {};
$(document).ready(function() {
	var containerAverageRentalPrice = 'average-rental-price';
	charts[containerAverageRentalPrice] = Highcharts.chart(containerAverageRentalPrice, {
		chart: {
			type: 'column',
		},
		title: {
			text: 'Average rental price in Barcelona (Spain)'
		},
		subtitle: {
			text: ''
		},
		xAxis: {
			categories: [],
			crosshair: true
		},
		yAxis: {
			min: 0,
			title: {
				text: 'Price in Euros'
			}
		},
		tooltip: {
			headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
				'<td style="padding:0"><b>{point.y: .1f} €</b></td></tr>',
			footerFormat: '</table>',
			shared: true,
			useHTML: true
		},
		plotOptions: {
			column: {
				pointPadding: 0.2,
				borderWidth: 0
			}
		},
		series: [],
		credits: {
			enabled: false
		},
	});
	charts[containerAverageRentalPrice].showLoading();

	var containerAverageOccupancy = 'average-occupancy';
	charts[containerAverageOccupancy] = Highcharts.chart(containerAverageOccupancy, {
		chart: {
			type: 'column',
		},
		title: {
			text: 'Average occupancy in Barcelona (Spain)'
		},
		subtitle: {
			text: ''
		},
		xAxis: {
			categories: [],
			crosshair: true
		},
		yAxis: {
			min: 0,
			title: {
				text: 'Population'
			}
		},
		tooltip: {
			headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
				'<td style="padding:0"><b>{point.y}</b></td></tr>',
			footerFormat: '</table>',
			shared: true,
			useHTML: true
		},
		plotOptions: {
			column: {
				pointPadding: 0.2,
				borderWidth: 0
			}
		},
		series: [],
		credits: {
			enabled: false
		},
	});
	charts[containerAverageOccupancy].showLoading();


	var containerAverageTouristOccupancy = 'average-tourist-occupancy';
	charts[containerAverageTouristOccupancy] = Highcharts.chart(containerAverageTouristOccupancy, {
		chart: {
			type: 'column'
		},
		title: {
			text: 'Average occupancy in Barcelona (Spain)'
		},
		subtitle: {
			text: ''
		},
		xAxis: {
			categories: [],
			crosshair: true
		},
		yAxis: {
			min: 0,
			title: {
				text: 'Population'
			}
		},
		tooltip: {
			headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
				'<td style="padding:0"><b>{point.y}</b></td></tr>',
			footerFormat: '</table>',
			shared: true,
			useHTML: true
		},
		plotOptions: {
			column: {
				pointPadding: 0.2,
				borderWidth: 0
			}
		},
		series: [],
		credits: {
			enabled: false
		},
	});
	charts[containerAverageTouristOccupancy].showLoading();

	requestDataAverageRentalPrice(containerAverageRentalPrice, 1, function(id, data){
		updateChartsTypeColumn(id, data);
		updateCardDeck('average-rental-price-years', data);
	});
	requestDataAverageRentalPrice(containerAverageOccupancy, 2, updateChartsTypeColumn);
	requestDataAverageRentalPrice(containerAverageTouristOccupancy, 3, updateChartsTypeColumn);
});
