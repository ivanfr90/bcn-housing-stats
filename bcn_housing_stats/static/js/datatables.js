
function initDatatable(id, resourceType, resourceTypeSlug) {
	var headersFields = headers(resourceTypeSlug);
	if (headers) {
		$(`#table-${id}`).DataTable({
			"processing": true,
			"serverSide": true,
			"ajax": {
				url: `${ENDPOINT_RESOURCE_DATA}/${resourceType}?flat=true`,
				method: "GET"
			},
			"columns": headersFields
		});
	}
}

function headers(resourceTypeSlug) {
	var columns;
	if(resourceTypeSlug == AVERAGE_MONTHLY_RENT) {
		columns = [
			{ data: "concept" },
			{ data: "code_district" },
			{ data: "name_district" },
			{ data: "code_neighborhood" },
			{ data: "name_neighborhood" },
			{ data: "quarter" },
			{ data: "price" },
			{ data: "year" }
		];
	} else if (resourceTypeSlug == AVERAGE_OCCUPANCY) {
		columns = [
			{ data: "code_district" },
			{ data: "name_district" },
			{ data: "code_neighborhood" },
			{ data: "name_neighborhood" },
			{ data: "houses" },
			{ data: "residents" },
			{ data: "average_occupancy" },
			{ data: "year" }
		];
	} else if (resourceTypeSlug == TOURIST_OCCUPANCY) {
		columns = [
			{ data: "name_district" },
			{ data: "name_neighborhood" },
			{ data: "accommodation_type" },
			{ data: "price" },
			{ data: "availability" }
		];
	}
	return columns;
}
