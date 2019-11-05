
var charts = {};
$(document).ready(function() {
	var containerAverageRentalPrice = 'average-rental-price';
	charts[containerAverageRentalPrice] = Highcharts.chart(containerAverageRentalPrice, {
		chart: {
			type: 'column',
			events: {
                load: requestDataAverageRentalPrice(containerAverageRentalPrice, 1)
            }
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
			events: {
                load: requestDataAverageRentalPrice(containerAverageOccupancy, 2)
            }
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
			type: 'column',
			events: {
                load: requestDataAverageRentalPrice(containerAverageTouristOccupancy, 3)
            }
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
});
