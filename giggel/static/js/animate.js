$(function() {
  $('#main').click(function() {

    if ($('#main').hasClass('inactive')) {
    $('#main').addClass('active');
    $('#main').removeClass('inactive');
    $('.animatable').addClass('animate');
      $('.animatable').removeClass('deanimate');
      $('.click').addClass('hide');
    }
    else {
       $('#main').addClass('inactive');
    $('#main').removeClass('active');
      $('.animatable').removeClass('animate');
      $('.animatable').addClass('deanimate');
      $('.click').removeClass('hide');
    }

  });
});
