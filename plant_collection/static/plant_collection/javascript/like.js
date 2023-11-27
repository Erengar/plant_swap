// This file is used to like a plant and update the number of likes
$('.heart').on('click', _.throttle(function() {
    var plant = $(this).attr('data-plant');
    var user = $(this).attr('data-user');
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        type:'post',
        url:'/like/',
        data:{plant: plant,
            user: user,
            csrfmiddlewaretoken: csrf},
        success: function (response) {
            if ($(`.heart[data-plant='${plant}'] > i.has-text-danger`).hasClass('fa-regular') && response) {
                $(`.heart[data-plant='${plant}'] > i.has-text-danger`).removeClass('fa-regular fa-heart');
                $(`.heart[data-plant='${plant}'] > i.has-text-danger`).addClass('fa-solid fa-heart');
            } else if ($(`.heart[data-plant='${plant}'] > i.has-text-danger`).hasClass('fa-solid') && response) {
                $(`.heart[data-plant='${plant}'] > i.has-text-danger`).removeClass('fa-solid fa-heart');
                $(`.heart[data-plant='${plant}'] > i.has-text-danger`).addClass('fa-regular fa-heart');
            }
            $(`.number_likes[data-plant='${plant}']`).html(response+' like/s');
          }
        });
      },300));
    