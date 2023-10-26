$('.sendable').on('click', _.throttle(function() {

    if($(this).hasClass('red-check')) {
        var finalize = true;
    } else if($(this).hasClass('green-check')) {
        var finalize = false;
    }

    var offerer = $('#offerer').text();
    var requester = $('#requester').text();
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var self = $(this);
    var errorTag = $('.form.column')
    
    $.ajax({
        type: 'post',
        url: '',
        data : {
            finalize: finalize,
            offerer: offerer,
            requester: requester,
            csrfmiddlewaretoken: csrf,
        },
        beforeSend: function(){
            $(self).removeClass('fa-solid fa-circle-check');
            $(self).addClass('fas fa-spinner fa-spin');
        },
        success: function(response){
            $(self).removeClass();
            $(self).addClass(response);
        },
        error: function(response){
            errorTag.append('<p class="error has-text-danger">Something went wrong. Please try again.</p>');
        }

    })
}, 300));