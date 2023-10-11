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
    
    $.ajax({
        type: 'post',
        url: '',
        data : {
            finalize: finalize,
            offerer: offerer,
            requester: requester,
            csrfmiddlewaretoken: csrf,
        },
        success: function(response){
            $(self).removeClass();
            $(self).addClass(response);
        }
    })
}, 300));