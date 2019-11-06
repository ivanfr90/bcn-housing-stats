
var charts = {};

// charts containers id
var containerBasicLineAverageRentalPricePerYearsID = 'average-rental-price-per-years-basic-line';
var containerBasicLineAccommodationsRentalsPerYearsID = 'accommodations-per-year-basic-line';
var containerBasicLineResidentsPerYearsID = 'residents-per-year-basic-line';
var containerAverageRentalPriceColumnVerticalID = 'average-rental-price-column-vertical';
var containerAverageOccupancyColumnVerticalID = 'average-occupancy-column-vertical';
var containerAverageTouristOccupancyColumnVerticalID = 'average-tourist-occupancy-column-vertical';

// charts function declarations
var columnVerticalChart;
var basicLine;

columnVerticalChart = function(containerId, title, yAxisTitle, format, units) {
	charts[containerId] = Highcharts.chart(containerId, {
		chart: {
			type: 'column',
		},
		title: {
			text: title
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
				text: yAxisTitle
			}
		},
		tooltip: {
			headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
				'<td style="padding:0"><b>{point.y: ' + format + '} ' + units + '</b></td></tr>',
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
	charts[containerId].showLoading();
};

basicLine = function (containerId, title, yAxisTitle, format, units) {
	charts[containerId] = Highcharts.chart(containerId, {
		chart: {
			type: 'line'
		},
		title: {
			text: title
		},
		xAxis: {
			categories: []
		},
		yAxis: {
			title: {
				text: yAxisTitle
			}
		},
		tooltip: {
			headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
				'<td style="padding:0"><b>{point.y: ' + format + '} ' + units + '</b></td></tr>',
			footerFormat: '</table>',
			shared: true,
			useHTML: true
		},
		plotOptions: {
			line: {
				dataLabels: {
					enabled: true
				},
				enableMouseTracking: true
			},
			series: {
            	allowPointSelect: false
			}
		},
		series: [{
			name: 'Barcelona',
    		data: [],
    		lineWidth: 5
		}],
		credits: {
			enabled: false
		},
	});
	charts[containerId].showLoading();
};

// charts functions

function updateChartsTypeColumnVertical(id, data, key) {
	data = data[key];
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
};

function updateChartsTypeBasicLine(id, data, key) {
	data = data[key];
	var dataSeries = [];
	$.each(data.series, function(i, serie) {
		dataSeries.push(parseFloat(serie.value.toFixed(2)))
	});

	charts[id].series[0].setData(dataSeries);

	charts[id].xAxis[0].update({
		categories: data.categories
	}, true);

	charts[id].hideLoading();
};
