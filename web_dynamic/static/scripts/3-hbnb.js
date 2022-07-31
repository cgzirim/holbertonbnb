// Dynamically filter amenities
$(function () {
  const amenities = {};
  $('.amenities input').change(function () {
	  if ($(this).is(':checked')) {
      amenities[$(this).attr('data-id')] = $(this).attr('data-name');
	  } else {
      delete amenities[$(this).attr('data-id')];
	  }
	  if (Object.values(amenities).length === 0) {
      $('.amenities H4').html('&nbsp');
	  } else {
      $('.amenities H4').text(Object.values(amenities).join(', '));
	  }
  });

  // Dynamically change API status
  $.get('http://localhost:5001/api/v1/status/', (data) => {
	  if (data.status === 'OK') {
      $('DIV#api_status').addClass('available');
	  } else {
      $('DIV#api_status').removeClass('available');
	  }
  });
});

// Fetch places dynamically
$(function () {
  $.ajax({
    type: 'POST',
    url: 'http://0.0.0.0:5001/api/v1/places_search/',
    contentType: 'application/json',
    data: '{}',
    dataType: 'json',
    success: uploadPlaces
  });
});

// Function to dynamically upload places
function uploadPlaces (data) {
  $('section.places').empty();
  $('section.places').append('<h1>Places</h1>');
  $.get('http://0.0.0.0:5001/api/v1/users', function (response) {
    const users = response;
    for (const place of data) {
      const user = users.find(user => user.id === place.user_id);
      let s = 's';
      if (place.number_rooms == 1 || place.number_bathrooms == 1 || place.max_guest == 1) {
        s = '';
      }
      $('section.places').append(
				`<article>
					<div class="headline">
						<h2>${place.name}</h2>
						<div class="price_by_night">$${place.price_by_night}</div>
					</div>
					<div class="information">
						<div class="max_guest">
							<div class="guest_icon"></div>
							<p>${place.max_guest} Guest${s}</p>
						</div>
						<div class="number_rooms">
							<div class="bed_icon"></div>
							<p>${place.number_rooms} Bedroom${s}</p>
						</div>
						<div class="number_bathrooms">
							<div class="bath_icon"></div>
							<p>${place.number_bathrooms} Bathroom${s}</p>
						</div>
					</div>
					<div class="user"><b>Owner</b>: ${user.first_name} ${user.last_name}</div>
					<div class="description">
						${place.description}
					</div>
			</article>`
      );
    }
  });
}
