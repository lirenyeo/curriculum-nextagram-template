$(document).ready(function() {
  $('#help-link').on('click', function(e) {
    e.preventDefault()
    $('body').addClass('sucked-into-blackhole')
    setTimeout(function() {
      $('body').remove()
    }, 1000)
  })

})