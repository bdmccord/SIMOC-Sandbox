$(document).ready(function () {
  $('.menu').on('click', function() {
      $('#mySidenav').toggleClass('opened');
  });

  $('.closebtn').on('click', function() {
      $('#mySidenav').toggleClass('opened');
  });

  setTimeout(function(){
    $('#sidebar').append("<div style='margin-bottom: 50px;'></div>");
  }, 500);
});
