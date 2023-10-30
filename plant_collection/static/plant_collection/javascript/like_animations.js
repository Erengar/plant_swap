$('.fa-heart.has-text-danger').on('click', function() {
    if($(this).hasClass('fa-regular') && $('a[href="/accounts/logout/"]').length){
    $(this).addClass('animation');
    setTimeout(() => {
        $(this).removeClass('animation');
    }, 300)
    };
    console.log($('a[href="accounts/logout"]'))
    
});