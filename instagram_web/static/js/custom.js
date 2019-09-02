$(document).ready(function() {
  $('#troll-button').on('click', function(e) {
    e.preventDefault()
    alert('Click OK to leave me forever')
    $('body').addClass('sucked-into-blackhole')
    setTimeout(function() {
      $('body').remove()
    }, 1000)
  })

  $('.grid').masonry({
    // options
    itemSelector: '.grid-item',
  });


})