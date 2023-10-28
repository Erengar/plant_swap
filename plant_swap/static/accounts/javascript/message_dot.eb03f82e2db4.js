let numberOfDots = $('.dot').length -1;
dots = $('.dot')
console.log(numberOfDots)

for (let i=0; i<numberOfDots; i++) {
    dots[i].remove()
}