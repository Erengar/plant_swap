const pictures = document.querySelectorAll('.carousel_image');
    const rightBtn = document.getElementById('right-arrow');
    const leftBtn = document.getElementById('left-arrow');
    var position = 0;

    for (let i = 1; i < pictures.length; i++) {
        pictures[i].setAttribute('hidden', true);
    }

    function hide() {
        for (let i = 0; i < pictures.length; i++) {
            pictures[i].setAttribute('hidden', true);
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