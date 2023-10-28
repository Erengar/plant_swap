let touchstartX = 0
let touchendX = 0

function checkDirection() {
    let delta = Math.abs(touchendX - touchstartX)
    if ((touchendX > touchstartX) && (delta > 150)) {
        if ($('#spiece-search-bar').hasClass('is-hidden-touch')){
            $('#spiece-search-bar').removeClass('is-1');
            $('#spiece-search-bar').removeClass('is-hidden-touch');
            $('#spiece-search-bar').addClass('is-full');
            $('#main-window').removeClass('is-11');
            $('#main-window').addClass('is-0');
    
        } 
    } else if ((touchendX < touchstartX) && (delta > 150)) {
        $('#spiece-search-bar').removeClass('is-full');
        $('#spiece-search-bar').addClass('is-1');
        $('#spiece-search-bar').addClass('is-hidden-touch');
        $('#main-window').removeClass('is-0');
        $('#main-window').addClass('is-11');
    }
  }

document.addEventListener('touchstart', e => {
    touchstartX = e.changedTouches[0].screenX
  })
  
document.addEventListener('touchend', e => {
    touchendX = e.changedTouches[0].screenX
    checkDirection()
})