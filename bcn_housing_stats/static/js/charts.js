
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
var donutChart;

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


donutChart = function (containerId, title, titleSeries, titleSubSeries) {
	charts[containerId] = Highcharts.chart(containerId, {
		chart: {
			type: 'pie'
		},
		title: {
			text: title
		},
		plotOptions: {
			pie: {
				shadow: false,
				center: ['50%', '50%']
			}
		},
		tooltip: {
			valueSuffix: '%'
		},
		series: [{
			name: titleSeries,
			data: [],
			size: '60%',
			dataLabels: {
				formatter: function () {
					return this.y > 5 ? this.point.name : null;
				},
				color: '#ffffff',
				distance: -30
			}
		}, {
			name: titleSubSeries,
			data: [],
			size: '80%',
			innerSize: '60%',
			dataLabels: {
				formatter: function () {
					// display only if larger than 1
					return this.y > 1 ? '<b>' + this.point.name + ':</b> ' +
						this.y + '%' : null;
				}
			},
			id: 'versions'
		}],
		responsive: {
			rules: [{
				condition: {
					maxWidth: 400
				},
				chartOptions: {
					series: [{
					}, {
						id: 'versions',
						dataLabels: {
							enabled: false
						}
					}]
				}
			}]
		},
		credits: {
			enabled: false
		},
	});
	charts[containerId].showLoading();
}

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

function updateDonutChart(id, data, key, year) {
	data = data[key];
	var series = [];
	var chartColors = Highcharts.getOptions().colors;
	var chartCategories = [];
	var chartData = [];
	var total = 0;

	for (var i=0; i<data.length; i++) {
		if (data[i]['year'] == year) {
			series = data[i].serie;
			break;
		}
	};

	series.forEach(function (item, key) {
		total += item['data'].reduce((a, b) => a + b, 0);
	});

	series.forEach(function (item, key) {
		item['data'].forEach(function (part, index) {
			item['data'][index] = part * 100 / total;
		});
	});

	series.forEach(function (item, key) {
		chartCategories.push(item['name']);
		chartData.push({
			y: item['data'].reduce((a, b) => a + b, 0),
			color: chartColors[key],
			drilldown: item
		})
	});

	var browserData = [];
	var versionsData = [];
	var drillDataLen;
	var brightness;

	// Build the data arrays
	for (var i = 0; i < chartData.length; i += 1) {
		// add browser data
		browserData.push({
			name: chartCategories[i],
			y: parseFloat(chartData[i].y.toFixed(2)),
			color: chartData[i].color
		});

		// add version data
		drillDataLen = chartData[i].drilldown.data.length;
		for (var j = 0; j < drillDataLen; j += 1) {
			brightness = 0.2 - (j / drillDataLen) / 5;
			versionsData.push({
				name: chartData[i].drilldown.categories[j],
				y: parseFloat(chartData[i].drilldown.data[j].toFixed(2)) ,
				color: Highcharts.Color(chartData[i].color).brighten(brightness).get()
			});
		}
	}

	charts[id].series[0].setData(browserData);
	charts[id].series[1].setData(versionsData);

	charts[id].hideLoading();
};
