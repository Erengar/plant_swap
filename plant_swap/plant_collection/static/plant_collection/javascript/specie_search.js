$('#ajax-search').on('keyup', _.throttle(function() {
    var search = $(this).val();


    $.ajax({
        type:'get',
        url:'http://127.0.0.1:8000/species/search/bar/',
        data:{search: search,
   },
        success: function (response) {
            $('.menu-list').html(response);
          },
        });
      }, 100));