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
});
