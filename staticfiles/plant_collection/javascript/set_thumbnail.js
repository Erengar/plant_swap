function hideSelect(){
    $('.selected').removeClass('selected');
}

$('.thumbnail').on('click', function() {
    hideSelect();
    $(this).addClass('selected');
    $('#thumbnail').prop('value', $(this).prop('id'));
})