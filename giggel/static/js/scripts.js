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

$('.star').click( function()  {
  $( this ).toggleClass('fa clicked');
})
