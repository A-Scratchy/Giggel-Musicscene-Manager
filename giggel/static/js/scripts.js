// on page load

$(function() {
$(".datePicker" ).datepicker();
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(function () {
  $('[data-toggle="popover"]').popover()
})

$('.fill').click( function()  {
  $( this ).toggleClass('fa clicked');
})

$('.mail').click( function()  {
  window.alert('sending email...')
})
