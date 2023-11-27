    /*
    In this script we are listening to input_container class for any change, that is file input.
    Once image is inserted into input, we display it, then hide used input tag and spawn new one.
    In this way we are protecting input tags from getting new image which would be messing with our display of images and event listener.
    Cross on the picture also removes given picture from post request.
    */


    const output = document.querySelector('output');
    var input = document.querySelector('.input_tag0');
    const inputContainer = document.querySelector('#replicator');
    const imageError = document.getElementById('#image-error');
    let count = 0;
    let counti = 0;
    let imagesArray = [];

    //Listening to object that will contain all file input fields, „change“ should be fine as long as we are adding and hiding fields
    inputContainer.addEventListener("change", () => {
        var files = input.files
        imagesArray.push(files)
        displayImages()
        addInput()
        removeInput()
      })

    /**
     * This function hides input field after image is uploaded
     */
    function removeInput() {
        let node = document.getElementById(`hiding${counti}`);
        let hid = document.createAttribute('hidden');
        node.setAttributeNode(hid);
        counti ++
        $('.image-error').remove()

    }
    
    /**
     * This function adds new input field after image is uploaded
     */
    //Needs different variable, because it starts counting from 1, as 0 is already placed in html
    function addInput() {
        count ++
        const inputHtml = document.createRange().createContextualFragment(
                            `<div class='field' id='hiding${count}'>
                            <div id='file-js-example' class='file is-medium'>
                                <label class='file-label pt-3'>
                                    <input class='input_tag${count} file-input' id='input_tag${count}' hidden type='file' accept='image/*' name='picture${count}'>
                                    <span class='file-cta'>
                                        <span class='file-icon'>
                                            <i class='fa-solid fa-image'></i>
                                        </span>
                                        <span class='file-label'>
                                            Upload image...
                                        </span>
                                    </span>
                                </label>
                            </div>
                        </div>`);
        //before was innerHtml +=, turned out it was invalidating input fields
        inputContainer.appendChild(inputHtml);
        input = document.querySelector(`.input_tag${count}`);
    }

    /**
     * This function displays images in the output div
     */
    function displayImages() {
        let images = "";
        imagesArray.forEach((image, index) => {
            for (let i = 0; i < image.length; i++) {
                images += `<div class='column is-6 is-4-widescreen'>
                                <div class='card-image'>
                                    <div class="image is-4by3">
                                        <img src="${URL.createObjectURL(image[i])}" alt="Picture of a plant">
                                        <span style='mix-blend-mode: difference' tabindex=0 onclick="deleteImage(${index}, ${i})">&times;</span>
                                    </div>
                                </div>
                            </div>`;
            }
        });
        output.innerHTML = images;
    }

    /**
     * This function deletes image from imagesArray and calls displayImages() to display images again
     * @param {string} index 
     */
    function deleteImage(index) {
        let nod = document.getElementById(`input_tag${index}`);
        let dis = document.createAttribute('disabled');
        nod.setAttributeNode(dis)
        imagesArray.splice(index, 1)
        displayImages()
      }
