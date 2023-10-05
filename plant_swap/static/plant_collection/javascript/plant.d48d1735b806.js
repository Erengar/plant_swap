$('.modal_open').on('click', function() {
    $('.modal').addClass('is-active')
});
$('.modal-close').on('click', function() {
    $('.modal').removeClass('is-active')
})
$('.modal-background').on('click', function() {
    $('.modal').removeClass('is-active')
})