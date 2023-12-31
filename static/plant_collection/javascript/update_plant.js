var data = []


let count = 0
hide()
existing_img()
$('#replicator').on('change', function() {
    displayImage();
    removeInput();
    addInput();
    hide();
    existing_img();
})



function removeInput() {
    $('.input_container > .to-hide').hide()
}


/*This adds new input field, once the old one is full. There is probably much better way to do this.*/
function addInput() {
    count ++
    $('#replicator').append(
                        `<div class='field to-hide' id='hiding${count}'>
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
}


/*Serves for displaying only images that were not before in database*/
function displayImage() {
    files = $(`.input_tag${count}`)[0].files;
    if (files.length > 0) {
        $('.columns').append(`<div class='column is-3-widescreen is-4-desktop'>
                                <div class='card-image'>
                                    <div class="image is-4by3">
                                        <img src="${URL.createObjectURL(files[0])}" alt="Picture of a plant">
                                        <span tabindex=0 class='delete' data-delete='${count}' style="position: absolute; top: 0; right: 0; mix-blend-mode: difference"></span>
                                    </div>
                                </div>
                            </div>`);
    }
}


/*Image is being hidden upon clicking on delete button.*/
function hide() {
    $('.delete').on('click', function() {
        $(this).parent().parent().hide()
    })
}


/*We are deleting images through delete button. If image is in database we store its name in array 'data'.
If given image is not yet in database we also disable its input.*/
function existing_img() {
    $('.delete').on('click', function(){
        if ($(this).siblings('img').attr('data-pic')) {
        data.push($(this).siblings('img').attr('data-pic'));
        } else {
            unupload = $(this).attr('data-delete');
            $(`.input_tag${unupload}`).attr('disabled', true);
        }
    })
}


/*Data is array of those images that we want to delete from database.
We are storing this array in child of #submit_btn with name 'to_delete' and value being the array*/
$('.columns').on('click', function(){
    $("#submit-btn > input[name='to delete']").remove();
    $("#submit-btn").append(`<input name='to delete' value="${data}" hidden>`);
})