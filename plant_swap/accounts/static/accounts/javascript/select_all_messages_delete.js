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