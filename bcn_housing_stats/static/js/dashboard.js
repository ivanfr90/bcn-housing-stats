// start function
var typeSelected = DEFAULT_TO_INIT;
$(document).ready(function() {
	(loadAndRender)();
});

function loadAndRender() {
	var selector = '';
	if (typeSelected === HISTORIC_DATA) {
		selector = 'historic-data-year';
	} else if (typeSelected === SIMPLE_DATA) {
		selector = 'simple-data-year';
	}

	checkedOptions = $(`input[name=${selector}]:checked`).map(function () {
		return this.value;
	}).get();

	cleanContainerChars();
	reloadCharts(checkedOptions);
};

function cleanContainerChars() {
	$(`#${CHART_CONTAINER}`).empty();
};

function reloadCharts(checkedOptions) {
	if (typeSelected === HISTORIC_DATA) {
		renderHistoricData(checkedOptions);
	} else if (typeSelected === SIMPLE_DATA) {
		renderSimpleData(checkedOptions);
	}
};

function createChartContainer(containerId, id) {
	$(`#${containerId}`).append(
		$('<div/>', {
			"class": 'row py-2'
		}).append($('<div/>', {
			"class": 'col'
		}).append($('<div/>', {
			"id": id,
			"class": "border"
		})))
	);
};

function createRow(rowId) {
	$(`#${CHART_CONTAINER}`).append(
		$('<div/>', {
			"id": rowId,
			"class": 'row py-2'
		})
	);
};

function createCol(id, rowId, col) {
	$(`#${rowId}`).append(
		($('<div/>', {
			"class": col
		}).append($('<div/>', {
			"id": id,
			"class": "border"
		})))
	);
};

function createSection(sectionId, title) {
	$(`#${CHART_CONTAINER}`).append(
		$('<div/>', {
			"class": 'd-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom'
		}).append($('<h3/>', {
			"text": title
		}))).append($('<div/>', {
			"id": sectionId,
			"class": ""
		})
	);
};

function updateCardDecksGrowthRate(id, data, key) {
	if (data[key] != 0) {
		$('#' + id).each(function () {
		var $this = $(this);
			jQuery({ Counter: 0 }).animate({ Counter: data[key] }, {
				duration: 1000,
				easing: 'swing',
				step: function () {
					$this.text(`${this.Counter.toFixed(2)} %`);
			}
			});
		});
	} else {
		$('#' + id).text('-');
	}
};

function renderHistoricData(years) {

	createRow('single-charts');
	createCol(containerBasicLineAverageRentalPricePerYearsID, 'single-charts', 'col-4');
	basicLine(containerBasicLineAverageRentalPricePerYearsID,
		'Historic Housing Rental Price Growth by Years',
		'Housing rental price',
		'.1f',
		'€');

	createCol(containerBasicLineResidentsPerYearsID, 'single-charts', 'col-4');
	basicLine(containerBasicLineResidentsPerYearsID,
		'Historic Residents Growth by Years',
		'Residents',
		'.0f',
		'residents');

	createCol(containerBasicLineAccommodationsRentalsPerYearsID, 'single-charts', 'col-4');
	basicLine(containerBasicLineAccommodationsRentalsPerYearsID,
		'Historic Housing Tourist Rentals Growth by Years',
		'Rentals',
		'.0f',
		'accommodations');

	createChartContainer(CHART_CONTAINER, containerAverageRentalPriceColumnVerticalID, 'col');
	columnVerticalChart(containerAverageRentalPriceColumnVerticalID,
		'Average rental price in Barcelona (Spain)',
		'Price in Euros',
		'.1f',
		'€');

	createChartContainer(CHART_CONTAINER, containerAverageOccupancyColumnVerticalID, 'col');
	columnVerticalChart(containerAverageOccupancyColumnVerticalID,
		'Average occupancy in Barcelona (Spain)',
		'Population',
		'.0f',
		'residents');

	createChartContainer(CHART_CONTAINER, containerAverageTouristOccupancyColumnVerticalID, 'col');
	columnVerticalChart(containerAverageTouristOccupancyColumnVerticalID,
		'Average touristic rental accommodations in Barcelona (Spain)',
		'Accommodations (Entire apartment or rooms)',
		'.0f',
		'accommodations');

	requestData(1, years,function(data) {
		updateCardDecksGrowthRate(cardDeckGrowthRateHousingRentalPrice, data, 'growth_rate');
		updateChartsTypeColumnVertical(containerAverageRentalPriceColumnVerticalID, data, 'average_rental');
		updateChartsTypeBasicLine(containerBasicLineAverageRentalPricePerYearsID, data, 'average_rental_per_years');
		// updateCardDeck('average-rental-price-years', data);
	});

	requestData(2, years,function(data) {
		updateCardDecksGrowthRate(cardDeckGrowthRateResidents, data, 'growth_rate');
		updateChartsTypeColumnVertical(containerAverageOccupancyColumnVerticalID, data, 'average_residents');
		updateChartsTypeBasicLine(containerBasicLineResidentsPerYearsID, data, 'residents_per_years');
	});

	requestData(3, years,function(data){
		updateCardDecksGrowthRate(cardDeckGrowthRateTouristRentals, data, 'growth_rate');
		updateChartsTypeColumnVertical(containerAverageTouristOccupancyColumnVerticalID, data, 'tourist_rental_per_neighborhood');
		updateChartsTypeBasicLine(containerBasicLineAccommodationsRentalsPerYearsID, data, 'tourist_rentals_per_years');
	});
};

function renderSimpleData(years) {
	years.forEach(function (value) {
		createSection(`section-${value}`, value);
	});

	years.forEach(function (value) {
		createChartContainer(`section-${value}`, `donut-chart-touristic-rentals-concentration-${value}`, 'col');
		donutChart(`donut-chart-touristic-rentals-concentration-${value}`,
			'Concentration of touristic rentals accommodations in Barcelona (Spain)',
			'Districts',
			'Neighborhoods');

		createChartContainer(`section-${value}`, `pie-chart-touristic-rentals-type-${value}`, 'col');
		pieChart(`pie-chart-touristic-rentals-type-${value}`,
			'Touristic rentals accommodations types in Barcelona (Spain)',
			'Type');
	});

	requestData(3, years,function(data){
		years.forEach(function (value) {
			updateDonutChart(`donut-chart-touristic-rentals-concentration-${value}`, data, 'tourist_rental_accommodations_per_years', value);
			updatePieChart(`pie-chart-touristic-rentals-type-${value}`, data, 'tourist_rental_accommodations_per_type', value);
		});
	});
};

