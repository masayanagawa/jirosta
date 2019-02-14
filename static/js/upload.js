$(function () {
    var val = $(".photo_form").val();
    if(!val){
        $(".data_submit_mask").addClass("mask_open");
        $(".modal_data_submit_mask").addClass("mask_open");
    } else {
        $(".data_submit_mask").removeClass("mask_open");
        $(".modal_data_submit_mask").removeClass("mask_open");
    }
})

var file = $(".uploadimg").change(function () {
    $(".data_submit_mask").removeClass("mask_open");
});

var file = $(".modal_uploadimg").change(function () {
    $(".modal_data_submit_mask").removeClass("mask_open");
});

$(".photo_form").bind("keyup",function(){
    var count = $(this).val().length;
    count = 300 - count;
    if(count < 0) {
        $(".text_count").css('color', 'red');
        $(".data_submit_mask").addClass("mask_open");
    } else {
        $(".text_count").css('color', 'black');
    }
    $(".text_count").text(count);
    
});

$(".modal_photo_form").bind("keyup",function(){
    $(".modal_text_count").text("300");
    var count = $(this).val().length;
    count = 300 - count;
    if(count < 0) {
        $(".text_count").css('color', 'red');
        $(".data_submit_mask").addClass("mask_open");
    } else {
        $(".text_count").css('color', 'black'); 
    }

    $(".modal_text_count").text(count);
    
});


$('.uploadimg').change(function(){
    if (this.files.length > 0) {
        var file = this.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function() {
            $('#preview').attr('src', reader.result );
            $('#preview').addClass('cover');
            $("#preview").removeClass("mask_open");
        }
    }
});

$('.modal_uploadimg').change(function(){
    if (this.files.length > 0) {
        var file = this.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        
        reader.onload = function() {
            $('#modal_preview').attr('src', reader.result );
            $('#modal_preview').addClass('cover');
            $("#modal_preview").removeClass("mask_open");
        }
    }
});
