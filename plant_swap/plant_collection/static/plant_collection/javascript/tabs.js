var url = window.location.href;


if (url.includes("my-collection")) {
    $('.navbar-item[href="/my-collection/"]').addClass("is-active");
} else if (url === 'http://127.0.0.1:8000/') {
    $('.navbar-item[href="/"]').addClass("is-active");
} else if (url.includes('species')) {
    var myspecie = url.split("/")[4];
    $('a[href="/species/' + myspecie + '/"]').addClass("is-active");
} else if (url.includes('accounts/trades')) {
    $('a[href="/accounts/trades/"]').addClass("is-active");
}