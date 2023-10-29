$('.fa-heart.has-text-danger').on('click', function() {
    if($(this).hasClass('fa-regular')){
    $(this).addClass('animation');
    setTimeout(() => {
        $(this).removeClass('animation');
    }, 300)
    };
    
});