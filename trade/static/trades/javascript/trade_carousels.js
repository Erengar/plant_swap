const pictures1 = document.querySelectorAll('.carousel_image1');
const rightBtn1 = document.getElementById('right-arrow1');
const leftBtn1 = document.getElementById('left-arrow1');
const carousel1 = $('.carousel-box:last');
var position1 = 0;
let touchstartX = 0
let touchendX = 0



for (let i = 1; i < pictures1.length; i++) {
    pictures1[i].setAttribute('hidden', true);
}

function hide1() {
    for (let i = 0; i < pictures1.length; i++) {
        pictures1[i].setAttribute('hidden', true);
    }
}

function checkDirection1() {
    let delta = Math.abs(touchendX - touchstartX)
    if ((touchendX > touchstartX) && (delta > 150)) {
        hide1();
        if (position1 == pictures1.length-1) {
            position1 = 0;
        } else {
            position1 ++;
        }
        pictures1[position1].removeAttribute('hidden');
        pictures1[position1].classList.add('faded');
    
    } else if ((touchendX < touchstartX) && (delta > 150)) {
        hide1();
        if (position1 == 0) {
            position1 = pictures1.length-1;
        } else {
            position1 --;
        }
        pictures1[position1].removeAttribute('hidden');
        pictures1[position1].classList.add('faded');
  }
}


rightBtn1.addEventListener('click', () => {
    hide1();
    if (position1 == pictures1.length-1) {
        position1 = 0;
    } else {
        position1 ++;
    }
    pictures1[position1].removeAttribute('hidden');
    pictures1[position1].classList.add('faded');
})

leftBtn1.addEventListener('click', () => {
    hide1();
    if (position1 == 0) {
        position1 = pictures1.length-1;
    } else {
        position1 --;
    }
    pictures1[position1].removeAttribute('hidden');
    pictures1[position1].classList.add('faded');
})


carousel1.on('touchstart', e => {
    touchstartX = e.changedTouches[0].screenX
  })
  
carousel1.on('touchend', e => {
    touchendX = e.changedTouches[0].screenX
    checkDirection1()
});





const pictures = document.querySelectorAll('.carousel_image');
const rightBtn = document.getElementById('right-arrow');
const leftBtn = document.getElementById('left-arrow');
const carousel = $('.carousel-box:first');
var position = 0;


for (let i = 1; i < pictures.length; i++) {
    pictures[i].setAttribute('hidden', true);
}


function hide() {
    for (let p = 0; p < pictures.length; p++) {
        pictures[p].setAttribute('hidden', true);
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
        pictures[position].classList.add('faded');
    
    } else if ((touchendX < touchstartX) && (delta > 150)) {
        hide();
        if (position == 0) {
            position = pictures.length-1;
        } else {
            position --;
        }
        pictures[position].removeAttribute('hidden');
        pictures[position].classList.add('faded');
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
    pictures[position].classList.add('faded');
})

leftBtn.addEventListener('click', () => {
    hide();
    if (position == 0) {
        position = pictures.length-1;
    } else {
        position --;
    }
    pictures[position].removeAttribute('hidden');
    pictures[position].classList.add('faded');
});


carousel.on('touchstart', e => {
    touchstartX = e.changedTouches[0].screenX
    })
    
carousel.on('touchend', e => {
    touchendX = e.changedTouches[0].screenX
    checkDirection()
});