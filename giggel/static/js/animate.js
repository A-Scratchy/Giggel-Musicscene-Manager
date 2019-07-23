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

  //   $('#artists').click(function() {
  //
  //     if ($('#artists').hasClass('inactive')) {
  //     $('#artists').addClass('active');
  //     $('#artists').removeClass('inactive');
  //     $('.subcircle').addClass('sub_animate');
  //       $('.subcircle').removeClass('desub_animate');
  //     }
  //     else {
  //        $('#artists').addClass('inactive');
  //     $('#artists').removeClass('active');
  //       $('.subcircle').removeClass('sub_animate');
  //       $('.subcircle').addClass('desub_animate');
  //     }
  // });

$('#login').click(function() {
    $('.lightbox').addClass('show');
    $('.lightbox').removeClass('hidden');
  });

$('.close').click(function() {
  $('.lightbox').removeClass('show');
  $('.lightbox').addClass('hidden');
});

});
