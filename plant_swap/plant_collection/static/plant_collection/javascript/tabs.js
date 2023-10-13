var url = window.location.href;


if (url.includes("my-collection")) {
    $('.navbar-item[href="/my-collection/"]').addClass("navbar-active");
} else if (url === 'http://127.0.0.1:8000/') {
    $('.navbar-item[href="/"]').addClass("navbar-active");
} else if (url.includes('species')) {
    var myspecie = url.split("/")[4];
    $('a[href="/species/' + myspecie + '/"]').addClass("sage-green");
} else if (url.includes('accounts/trades')) {
    $('a[href="/accounts/trades/"]').addClass("navbar-active");
} else if (url.includes('accounts/likes')) {
    $('a[href="/accounts/likes/"]').addClass("navbar-active");
}