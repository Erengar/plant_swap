$('.dropdown').on('click', function() {
    $('.dropdown').toggleClass('is-active');
});


$('.dropdown-item').on('click', function(){

    $.ajax({
        type: 'get',
        url: '/trade/123',
        data: {
            'plant': $(this).text(),
        },
        success: function(response){
            $('#dump').html(response);
            var offered_plant = $('.offered-plant').text()
            $('#offered').attr('value', offered_plant);
            const pictures = document.querySelectorAll('.carousel_image');
            for (let p = 1; p < pictures.length; p++) {
                pictures[p].setAttribute('hidden', true);
            }
        },
        error: function(response){
            $('#dump').html('Something went wrong!')
        },
        beforeSend: function(){
            $('#dump').html('<p class="title is-flex is-justify-content-center">Loading...</p>')
        }
    })
})