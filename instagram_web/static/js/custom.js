function followHandler(e) {
  e.preventDefault()
  $.ajax({
    url: `/users/${e.target.id}/follow`,
    method: 'GET',
    beforeSend: function() {
      $('.follow-btn')
        .prop('disabled', true)
        .text('Loading...')
    },
    success: function(response) {
      $('#followers-count').text(response.new_follower_count)
      $('.follow-btn')
        .prop('disabled', false)
        .removeClass('btn-info follow-btn')
        .addClass('btn-outline-info unfollow-btn')
        .text('Unfollow')
        .unbind('click')
        .on('click', unfollowHandler)
    }
  })
}

function unfollowHandler(e) {
  e.preventDefault()
  $.ajax({
    url: `/users/${e.target.id}/unfollow`,
    method: 'GET',
    beforeSend: function() {
      $('.follow-btn')
        .prop('disabled', true)
        .text('Loading...')
    },
    success: function(response) {
      $('#followers-count').text(response.new_follower_count)
      $('.unfollow-btn')
        .prop('disabled', false)
        .removeClass('btn-outline-info unfollow-btn')
        .addClass('btn-info follow-btn')
        .text('Follow')
        .unbind('click')
        .on('click', followHandler)
    }
  })
}

$(document).ready(function() {
  $('.follow-btn').on('click', followHandler)
  $('.unfollow-btn').on('click', unfollowHandler)


  $('#troll-button').on('click', function(e) {
    e.preventDefault()
    alert('Click OK to leave me forever')
    $('body').addClass('sucked-into-blackhole')
    setTimeout(function() {
      $('body').remove()
    }, 1000)
  })

  $('.grid').masonry({
    itemSelector: '.grid-item'
  })
})
