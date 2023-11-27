//This file contains the javascript for highlighting the active tab in the order menu
const order_url = window.location.href;

if(order_url.includes('likes') && !order_url.includes('-likes')) {
    $('#likes').addClass('is-active')
} else if(order_url.includes('created') && !order_url.includes('-created')) {
    $('#created').addClass('is-active')
} else if(order_url.includes('nick_name') && !order_url.includes('-nick_name')) {
    $('#nick_name').addClass('is-active')
} else if(order_url.includes('owner') && !order_url.includes('-owner')) {
    $('#owner').addClass('is-active')
} else if(order_url.includes('-created')) {
    $('#-created').addClass('is-active')
} else if(order_url.includes('-nick_name')) {
    $('#-nick_name').addClass('is-active')
} else if(order_url.includes('-owner')) {
    $('#-owner').addClass('is-active')
} else {
    $('#-likes').addClass('is-active')
}