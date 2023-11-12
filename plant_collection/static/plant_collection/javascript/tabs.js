var url = window.location.href;


if (url.includes("my-collection")) {
    $('.navbar-item[href="/my-collection/"]').addClass("navbar-active");
} else if ((url === 'http://127.0.0.1:8000/')||(url === 'https://plant-swap.onrender.com/')) {
    $('.navbar-item[href="/"]').addClass("navbar-active");
} else if (url.includes('species')) {
    var myspecie = url.split("/")[4];
    $('a[href="/species/' + myspecie + '/"]').addClass("sage-green");
    $('.navbar-item[href="/species/"]').addClass("navbar-active");
} else if (url.includes('/trades')) {
    $('.navbar-item[href="/trades/"]').addClass("navbar-active");
} else if (url.includes('accounts/likes')) {
    $('.navbar-item[href="/accounts/likes/"]').addClass("navbar-active");
} else if (url.includes('/accounts/messages/')) {
    $('.navbar-item[href="/accounts/messages/"]').addClass("navbar-active");
} else if (url.includes('accounts/profile')) {
    $('.navbar-item[href="/accounts/profile/"]').addClass("navbar-active");
} else if ((url.includes('accounts/registration') | url.includes('accounts/login'))) {
    $('.navbar-item[href="/accounts/login/"]').addClass("navbar-active");
}