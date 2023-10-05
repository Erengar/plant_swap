$('.heart').on('click', _.throttle(function() {
    var plant = $(this).attr('data-plant');
    var user = $(this).attr('data-user');
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var url = window.location.href;

    $.ajax({
        type:'post',
        url:'',
        data:{plant: plant,
            user: user,
            csrfmiddlewaretoken: csrf,
            url: url},
        success: function (response) {
            if ($(`.heart[data-plant='${plant}'] > i.has-text-danger`).hasClass('fa-regular') && response) {
                $(`.heart[data-plant='${plant}'] > i.has-text-danger`).removeClass('fa-regular fa-heart');
                $(`.heart[data-plant='${plant}'] > i.has-text-danger`).addClass('fa-solid fa-heart');
            } else if ($(`.heart[data-plant='${plant}'] > i.has-text-danger`).hasClass('fa-solid') && response) {
                $(`.heart[data-plant='${plant}'] > i.has-text-danger`).removeClass('fa-solid fa-heart');
                $(`.heart[data-plant='${plant}'] > i.has-text-danger`).addClass('fa-regular fa-heart');
            }
            $(`.number_likes[data-plant='${plant}']`).html(response+' like/s');
          },
        });
      },300));
    