$(document).ready(function () {
    
    $('#login-form').submit(function () {
        if($(this).valid()){
    
            var operation = "LOGIN";
            var datas = $(this).serialize() + "&operation=" + operation;
            $.ajax({
                type: 'POST',
                url: './',
                dataType: 'json',
                data: datas,
                beforeSend: function () {
                    $('#please-wait').css('display', 'block');
                    $('#error').css('display', 'none');
                },
                success: function (json) {
                    console.log(json);
                    $('#please-wait').css('display', 'none');
                    if (json.status === "success") {
                        $('#success').css('display', 'block');
                        window.open(json.url, "_self");

                    } else {

                        $('#error').html('<strong>'+json.message+'</strong>');
                        $('#error').css('display', 'block');
                    }

                },
                error: function (error) {
                    $('#please-wait').css('display', 'none');
                    alert("Error");
                    console.log(error);
                }
            });
        }
    });
    
    $('#change-password-form').submit(function () {
        if($(this).valid()){
            var operation = "CHANGE-PASSWORD";
            var datas = $(this).serialize() + "&operation=" + operation;
            $.ajax({
                type: 'POST',
                url: './',
                dataType: 'json',
                data: datas,
                beforeSend: function () {
                    $('#please-wait').css('display', 'block');
                    $('#error').css('display', 'none');
                },
                success: function (json) {
                    console.log(json);
                    $('#please-wait').css('display', 'none');
                    if (json.status === "success") {
                        $('#success').css('display', 'block');
                    } else {

                        $('#error').html('<strong>'+json.message+'</strong>');
                        $('#error').css('display', 'block');
                    }

                },
                error: function (error) {
                    $('#please-wait').css('display', 'none');
                    alert("Error");
                    console.log(error);
                }
            });
        }
    });
    
    
});


