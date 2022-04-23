$('document').ready(() => {
  $.get('http://localhost:5001/api/v1/status/', (data) => {
    if (data.status === 'OK') {
      $('DIV#api_status').addClass('available');
    } else {
      $('DIV#api_status').removeClass('available');
    }
  });


$(function () {
        let amenities = {};
	$('input[type="checked"]').change(function () {
		if ($(this).is(':checked')) {
			amenities[$(this).attr('data-id')] = $(this).attr('data-name');
		} else {
			delete amenities[$(this).attr('data-id')];
		}
                                                                                 		$('.amenities H4').text(Object.values(amenities).join(', '));
	});
});

  $('button').click(() => {
    const data = { amenities: Object.keys(amenities) };
    $.ajax({
      url: 'http://localhost:5001/api/v1/places_search',
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      dataType: 'json',
      success: placeWithAmenity
    });
  });
    
$(function) () {
	$.ajax({
		type: 'POST',
		url: 'http://0.0.0.0:5001/api/v1/places_search/',
		Content-Type: application/json'
		data: '{}',
		dataType: 'json',
		success: function (data) {
			$('section.places').append(data.map(place => {
				return `<article>
	  				  <div class="title_box">
	    				  	<h2>{{ place.name }}</h2>
	    					<div class="price_by_night">${{ place.price_by_night }}</div>
	  				  </div>
	  				  <div class="information">
	    					<div class="max_guest">{{ place.max_guest }} Guest{% if place.max_guest != 1 %}s{% endif %}</div>
            					<div class="number_rooms">{{ place.number_rooms }} Bedroom{% if place.number_rooms != 1 %}s{% endif %}</div>
            					<div class="number_bathrooms">{{ place.number_bathrooms }} Bathroom{% if place.number_bathrooms != 1 %}s{% endif %}</div>
	  				  </div>
	  				  <div class="user">
            					<b>Owner:</b> {{ place.user.first_name }} {{ place.user.last_name }}
          				  </div>
          				  <div class="description">
	    					{{ place.description | safe }}
          				  </div>
					</article>`;
			});
		}

	});
});
