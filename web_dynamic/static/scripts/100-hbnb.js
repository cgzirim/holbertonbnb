$('document').ready(() => {
  $.get('http://localhost:5001/api/v1/status/', (data) => {
    if (data.status === 'OK') {
      $('DIV#api_status').addClass('available');
    } else {
      $('DIV#api_status').removeClass('available');
    }
  });
  $.ajax({
    url: 'http://localhost:5001/api/v1/places_search',
    type: 'POST',
    data: '{}',
    contentType: 'application/json',
    dataType: 'json',
    success: placeWithAmenity
  });

    const amenities = {};
  const states = {};
  const cities = {};

  $('div.amenities li input').change(function () {
    if ($(this).is(':checked')) {
      amenities[($(this).attr('data-id'))] = $(this).attr('data-name');
    } else {
      delete amenities[($(this).attr('data-id'))];
    }
    $('div.amenities h4').text(Object.values(amenities).join(', '));
  });

  $('div.locations h2 > input').change(
        function () {
          if ($(this).is(':checked')) {
            states[($(this).attr('data-id'))] = $(this).attr('data-name');
          } else {
            delete states[($(this).attr('data-id'))];
          }
          const both = Object.values(states).concat(Object.values(cities));
          $('div.locations h4').html(both.join(', ') || '&nbsp;');
        });

  $('div.locations li > input').change(
    function () {
      if ($(this).is(':checked')) {
        cities[($(this).attr('data-id'))] = $(this).attr('data-name');
      } else {
        delete cities[($(this).attr('data-id'))];
      }
      const both = Object.values(states).concat(Object.values(cities));
      $('div.locations h4').html(both.join(', ') || '&nbsp;');
    });

  $('button').click(() => {
    const data = { 
      amenities: Object.keys(amenities),
      states: Object.keys(states),
      cities: Object.keys(cities)
    };
    $.ajax({
      url: 'http://localhost:5001/api/v1/places_search',
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      dataType: 'json',
      success: placeWithAmenity
    });
  });


  function placeWithAmenity (listPlaces) {
    $('.placeontainer').empty();
    for (const place of listPlaces) {
      $('.placeontainer').append(
        `<article>
          <div class="title_place">
            <h2>${place.name}</h2>
            <div class="price_by_night">
            ${place.price_by_night}
            </div>
          </div>
          <div class="details">
            <div class="max_guest">
              <div class="logo"></div>
              <span>${place.max_guest} Guests</span>
            </div>
            <div class="number_rooms">
              <div class="logo"></div>
              <span>${place.number_rooms} Bedroom</span>
            </div>
            <div class="number_bathrooms">
              <div class="logo"></div>
              <span>${place.number_bathrooms} Bathroom</span>
            </div>
          </div>
          <div class="description">
            ${place.description}
          </div>
        </article>`
      );
    }
  }
});
