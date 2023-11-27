// This file is used to search for species in the database and display them in the menu list
$('#ajax-search').on('keyup', _.debounce(function () {
    var search = $(this).val();

    console.log(search)
    $.ajax({
        type:'get',
        url:'/species/search/bar/',
        data:{search: search,
   },
        success: (response) => {
            $('.menu-list').html(response);
            const species_url = window.location.pathname.split('/')[1];
            if ((species_url != 'likes') && (species_url != '-likes')){
                $(`a[href*=${species_url}]`).addClass('is-active');
            }
          },
        error: (response) => {
          $('.menu-list').html('Something went wrong!')
          },
        beforeSend: () => {
          $('.menu-list').html('Loading...')
          }
        });
      }, 500));