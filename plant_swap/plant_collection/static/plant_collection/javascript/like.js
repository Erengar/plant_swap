$('.heart').on('click', function() {
    var plant
    var user
    var csrf
    var url
    plant = $(this).attr('data-plant');
    user = $(this).attr('data-user');
    csrf = $('input').attr('value');
    url = window.location.href;

    $.ajax({
        type:'POST',
        url:'',
        data:{plant: plant,
            user: user,
            csrfmiddlewaretoken: csrf,
            url: url},
        success: function (response) {
            if ($('i.has-text-danger').hasClass('fa-regular') && response) {
                $('i.has-text-danger').removeClass('fa-regular fa-heart');
                $('i.has-text-danger').addClass('fa-solid fa-heart');
            } else if ($('i.has-text-danger').hasClass('fa-solid') && response) {
                $('i.has-text-danger').removeClass('fa-solid fa-heart');
                $('i.has-text-danger').addClass('fa-regular fa-heart');
            }
            $('.number_likes').html(response+' like/s');
          },
        });
      });
    