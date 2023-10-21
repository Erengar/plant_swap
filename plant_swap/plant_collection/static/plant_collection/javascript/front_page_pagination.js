$('.pagination-link').on('click', function(){
    let page = $(this).contents().text();
    let pag = $(this);
    $.ajax({
        url: '',
        data: {
            'page': page
        },
        success: function(data){
            $('.column.is-11').html(data);
            $('.pagination-link').removeClass('is-current');
            $(pag).addClass('is-current');
        }
    })
})