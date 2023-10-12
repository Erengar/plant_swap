/*Have to make two carousels, because original that was made for plant view
works based of ID*/

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




/*Variables must be declared after element was inserted,
after offered plant is selected*/
function initializeDynamicElement() {
    
    const pictures1 = document.querySelectorAll('.carousel_image1');
    const rightBtn1 = document.getElementById('right-arrow1');
    const leftBtn1 = document.getElementById('left-arrow1');
    var position1 = 0;



    function hide1() {
        for (let p = 0; p < pictures1.length; p++) {
            pictures1[p].setAttribute('hidden', true);
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
    })

    leftBtn1.addEventListener('click', () => {
        hide1();
        if (position1 == 0) {
            position1 = pictures1.length-1;
        } else {
            position1 --;
        }
        pictures1[position1].removeAttribute('hidden');
    });
};


const targetElement = document.getElementById("dump");


const observer = new MutationObserver(function(mutationsList) {
    for (let mutation of mutationsList) {
        if (mutation.type === "childList") {
            for (let node of mutation.addedNodes) {
                initializeDynamicElement(node);
                }
            }
        }
    }
);


observer.observe(targetElement, { childList: true, subtree: true });