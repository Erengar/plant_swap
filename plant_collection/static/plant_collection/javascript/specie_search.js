$('#ajax-search').on('keyup', _.debounce(function () {
    var search = $(this).val();

    console.log(search)
    $.ajax({
        type:'get',
        url:'http://127.0.0.1:8000/species/search/bar/',
        data:{search: search,
   },
        success: (response) => {
            $('.menu-list').html(response);
          },
        error: (response) => {
          $('.menu-list').html('Something went wrong!')
          },
        beforeSend: () => {
          $('.menu-list').html('Loading...')
          }
        });
      }, 500));