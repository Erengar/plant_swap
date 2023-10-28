var check = false;

$('#select-all').on('click', function() {
    if (check == false) {
        $('.message-checkbox').prop('checked', true);
        check = true;
    } else {
        $('.message-checkbox').prop('checked', false);
        check = false;
    };
});


$('.message-checkbox').on('click', function(){
    if ($('.js-check:checked').length > 0) {
        $('.modal_open').removeAttr('disabled');
    } else {
        $('.modal_open').attr('disabled', true);
    }
})