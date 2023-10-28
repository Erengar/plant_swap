const pictures = document.querySelectorAll('.carousel_image');
const rightBtn = document.getElementById('right-arrow');
const leftBtn = document.getElementById('left-arrow');
const carousel = $('.carousel-box');
var position = 0;
let touchstartX = 0
let touchendX = 0

for (let i = 1; i < pictures.length; i++) {
    pictures[i].setAttribute('hidden', true);
}

function hide() {
    for (let i = 0; i < pictures.length; i++) {
        pictures[i].setAttribute('hidden', true);
    }
}


function checkDirection() {
    let delta = Math.abs(touchendX - touchstartX)
    if ((touchendX > touchstartX) && (delta > 150)) {
        hide();
        if (position == pictures.length-1) {
            position = 0;
        } else {
            position ++;
        }
        pictures[position].removeAttribute('hidden');
    
    } else if ((touchendX < touchstartX) && (delta > 150)) {
        hide();
        if (position == 0) {
            position = pictures.length-1;
        } else {
            position --;
        }
        pictures[position].removeAttribute('hidden');
  }
}

rightBtn.addEventListener('click', () => {
    hide();
    if (position == pictures.length-1) {
        position = 0;
    } else {
        position ++;
    }
    pictures[position].removeAttribute('hidden');
})

leftBtn.addEventListener('click', () => {
    hide();
    if (position == 0) {
        position = pictures.length-1;
    } else {
        position --;
    }
    pictures[position].removeAttribute('hidden');
})


carousel.on('touchstart', e => {
    touchstartX = e.changedTouches[0].screenX
  })
  
carousel.on('touchend', e => {
    touchendX = e.changedTouches[0].screenX
    checkDirection()
})