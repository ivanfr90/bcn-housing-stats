
var charts = {};

// chard decks id
var cardDeckGrowthRateHousingRentalPrice = 'growth-rate-housing-rental-price';
var cardDeckGrowthRateResidents = 'growth-rate-residents';
var cardDeckGrowthRateTouristRentals = 'growth-rate-tourist-rentals';

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
var pieChart;

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
				allowPointSelect: true,
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
};

pieChart = function (containerId, title, titleSeries) {
	charts[containerId] = Highcharts.chart(containerId, {
		chart: {
			plotBackgroundColor: null,
			plotBorderWidth: null,
			plotShadow: false,
			type: 'pie'
		},
		title: {
			text: title
		},
		tooltip: {
			pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
		},
		plotOptions: {
			pie: {
				allowPointSelect: true,
				cursor: 'pointer',
				dataLabels: {
					enabled: true,
					format: '<b>{point.name}</b>: {point.percentage:.1f} %',
					connectorColor: 'silver'
				},
				colors: Highcharts.map(Highcharts.getOptions().colors, function (color) {
					return {
						radialGradient: {
							cx: 0.5,
							cy: 0.3,
							r: 0.7
						},
						stops: [
							[0, color],
							[1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
						]
					};
				})
			}
		},
		series: [{
			name: titleSeries,
			data: []
		}]
	});
	charts[containerId].showLoading();
};


// charts functions

function updateChartsTypeColumnVertical(id, data, key) {
	data = data[key];
	data.series.forEach(function(seriesItem) {
		charts[id].addSeries({
			name: seriesItem.year,
			data: seriesItem.values
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
	data.series.forEach(function(seriesItem) {
		dataSeries.push(parseFloat(seriesItem.value.toFixed(2)))
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
			series = data[i].series;
			break;
		}
	};

	series.forEach(function (item) {
		total += item['data'].reduce((a, b) => a + b, 0);
	});

	series.forEach(function (item) {
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

function updatePieChart(id, data, key, year) {
	data = data[key];
	var series = [];
	var dataSeries = [];
	var total = 0;

	for (var i=0; i<data.length; i++) {
		if (data[i]['year'] == year) {
			series = data[i].series;
			break;
		}
	};

	series.forEach(function (item) {
		total += item['value'];
	});

	series.forEach(function (item) {
		item['value'] = item['value'] * 100 / total;
	});

	series.forEach(function(seriesItem) {
		dataSeries.push({
			'name': seriesItem['name'],
			'y': parseFloat(seriesItem.value.toFixed(2))
		});
	});

	charts[id].series[0].setData(dataSeries);

	charts[id].hideLoading();
}
