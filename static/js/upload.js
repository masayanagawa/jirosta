$(function () {
    var val = $(".photo_form").val();
    if(!val){
        $(".data_submit_mask").addClass("mask_open");
    }

    var file = $('.uploadimg')[0].files[0];
    if(!file){
        $(".data_submit_mask").addClass("mask_open");
    } else {
        $(".data_submit_mask").removeClass("mask_open");
    }

    // var file = this.files[0];
    // if(!file){
    //     $(".data_submit_mask").addClass("mask_open");
    // } else {
    //     $(".data_submit_mask").removeClass("mask_open");
    // }

})

$(".photo_form").bind("change keyup",function(){
    var count = $(this).val().length;
    count = 300 - count;
    if(count < 0) {
        $(".text_count").css('color', 'red');
        $(".data_submit_mask").addClass("mask_open");
    } else {
        $(".text_count").css('color', 'black');
        $(".data_submit_mask").removeClass("mask_open");
        // var file = $('.uploadimg')[0].files[0];
        // console.log(file);
        // if(!file){
        //     $(".data_submit_mask").addClass("mask_open");
        // } else {
        //     $(".data_submit_mask").removeClass("mask_open");
        // }
    }

    $(".text_count").text(count);
    
});




$('.uploadimg').change(function(){
    if (this.files.length > 0) {
        // 選択されたファイル情報を取得
        var file = this.files[0];
        // readerのresultプロパティに、データURLとしてエンコードされたファイルデータを格納
        var reader = new FileReader();
        reader.readAsDataURL(file);
        
        reader.onload = function() {
            $('.preview').attr('src', reader.result );
            $('.preview').addClass('cover');
        }
    }
});
