$(document).ready(function() {
  $('#troll-button').on('click', function(e) {
    e.preventDefault()
    alert('OH NO, WHAT HAVE YOU DONE!? HOLD ME TIGHTLY, IT GOT ME!')
    $('body').addClass('sucked-into-blackhole')
    setTimeout(function() {
      $('body').remove()
    }, 1000)
  })

})