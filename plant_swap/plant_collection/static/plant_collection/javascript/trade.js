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
            const pictures1 = document.querySelectorAll('.carousel_image1');
            for (let p = 1; p < pictures1.length; p++) {
                pictures1[p].setAttribute('hidden', true);
            }
        }
    })
})