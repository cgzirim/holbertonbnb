$(function () {
  // Dynamically filter amenities
  const amenities = {};
  $('.amenities input').change(function () {
	  if ($(this).is(':checked')) {
      amenities[$(this).attr('data-id')] = $(this).attr('data-name');
	  } else {
      delete amenities[$(this).attr('data-id')];
	  }
	  if (Object.values(amenities).length === 0) {
      $('.amenities h4').html('&nbsp;');
	  } else {
      $('.amenities h4').text(Object.values(amenities).join(', '));
	  }
  });

  // Dynamically filter states
  const states = {};
  $('.locations ul h2 input').change(function () {
	  if ($(this).is(':checked')) {
      states[$(this).attr('data-id')] = $(this).attr('data-name');
	  } else {
      delete states[$(this).attr('data-id')];
	  }
    const both = Object.assign({}, states, cities);
	  if (Object.values(both).length === 0) {
      $('.locations h4').html('&nbsp;');
	  } else {
      $('.locations h4').text(Object.values(both).join(', '));
	  }
  });

  // Dynamically filter cities
  const cities = {};
  $('.locations ul ul li input').change(function () {
	  if ($(this).is(':checked')) {
      cities[$(this).attr('data-id')] = $(this).attr('data-name');
	  } else {
      delete cities[$(this).attr('data-id')];
	  }
    const both = Object.assign({}, states, cities);
	  if (Object.values(both).length === 0) {
      $('.locations h4').html('&nbsp;');
	  } else {
      $('.locations h4').text(Object.values(both).join(', '));
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

  // Fetch places dynamically
  $.ajax({
    type: 'POST',
    url: 'http://0.0.0.0:5001/api/v1/places_search/',
    contentType: 'application/json',
    data: '{}',
    dataType: 'json',
    success: uploadPlaces
  });

  // Filter places by amenities
  $('button').click(function () {
    const data = {
      amenities: Object.keys(amenities),
      states: Object.keys(states),
      cities: Object.keys(cities)};
    $.ajax({
      url: 'http://localhost:5001/api/v1/places_search',
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
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
        // console.log(place)
        const amenities = [];
        $.get(`http://localhost:5001/api/v1/places/${place.id}/amenities`, function (response) {
          for (const amenity of response) {
            amenities.push(amenity.name);
          }
          // console.log(amenities)
        });
        const reviews = [];
        $.get(`http://localhost:5001/api/v1/places/${place.id}/reviews`, function (response) {
          for (const review of response) {
            if (review.place_id === place.id) {
              reviews.push([review.text, review.user_id, review.created_at]);
            }
          }
        });
        // console.log(reviews)
        // console.log(amenities)
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
					<h2 class="article_subtitle">Amenities</h2>
					<div class="amenities">
						<p>${place.description}</p>
					</div>
					<h2 class="article_subtitle">Reviews</h2>
					<div class="reviews">
						<ul>
							<li>
								<div class="review_item">
									<h3>From Bob Dylan the 27th January 2017</h3>
									<p class="review_text">Wow, what can I say?! I'm a real rolling stone, you may have heard, but - by golly - I'd just as well settle down in this humble home, if you'd part with it - course, I'm sure you wouldn't. Real shame too. Oh well...</p>
									<p> ${place.description} </p>
								</div>
							</li>
							<li>
								<div class="review_item">
									<h3>From Justin Majetich the 28th April 1991</h3>
									<p class="review_text">I was birthed in this here bathtub today!</p>
								</div>
							</li>
						</ul>
					</div>
			</article>`
        );
      }
    });
  }
});
