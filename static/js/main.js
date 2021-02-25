$(document).ready(function(){
    $("#sendpayment").submit(function(event){
        event.preventDefault();
        
        $.ajax({
            url: "/api/uploadpayment",
            method: "POST",
            data: new FormData($(this)[0]),
            cache: false,
            processData: false,
            contentType: false,
            success: function(data) {
                if(data.code == 200){
                    alert(data.message)
                    location.href = data.redirect
                }else{
                    alert(data.message)
                }
            },
            error: function(error){
                console.log(error);
            }
        })
    });
    
    $("#payment_show").click(function(event){
        event.preventDefault();

        var bookid = $(this).data("bookid")
        $.ajax({
            url: "api/payment_show",
            method: "POST",
            data: {bookid: bookid},
            dataType: "json",
            success: function(data) {
                if(data.code == 200){
                    $("#titlemodal").text("ชำระเงิน")
                    $("#dataresponse").html(data.html);
                    $("#showdata").modal("show");
                }else{
                    alert(data.message);
                    $("#login").modal("show");
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $("#inforoom").click(function(event){
        event.preventDefault();

        var roomid = $(this).data("roomid")
        $.ajax({
            url: "api/inforoom",
            method: "POST",
            data: {roomid: roomid},
            dataType: "json",
            success: function(data) {
                if(data.code == 200){
                    $("#titlemodal").text("ข้อมูลห้องพัก")
                    $("#dataresponse").html(data.html);
                    $("#showdata").modal("show");
                }else{
                    alert(data.message);
                    $("#login").modal("show");
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $("#infobook").click(function(event){
        event.preventDefault();

        var bookid = $(this).data("bookid")
        $.ajax({
            url: "api/infobooking",
            method: "POST",
            data: {bookid: bookid},
            dataType: "json",
            success: function(data) {
                if(data.code == 200){
                    $("#titlemodal").text("ข้อมูลห้องพัก")
                    $("#dataresponse").html(data.html);
                    $("#showdata").modal("show");
                }else{
                    alert(data.message);
                    $("#login").modal("show");
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $("#book").click(function(event){
        event.preventDefault();
        var roomid = $(this).data("roomid");

        $.ajax({
            url: "api/selectroom",
            method: "POST",
            data: {"roomid": roomid},
            dataType: "json",
            success: function(data) {
                if(data.code == 200) {
                    $("#titlemodal").text("จองห้องพัก")
                    $("#dataresponse").html(data.html);
                    $("#showdata").modal("show");
                }else{
                    alert(data.message);
                    $("#login").modal("show");
                }
            },
            error: function(error) {
                console.log(error);
            }
        })
    });

    $("#logindata").submit(function(event){
        event.preventDefault();

        var username = $("#username").val();
        var password = $("#password").val();

        $.ajax({
            url: "api/login",
            method: "POST",
            data: {username: username, password: password},
            dataType: "json",
            success: function(data) {
                alert(data.message)
                if(data.code == 200){
                    location.reload();
                }
            },
            error: function(error) {
                console.log(error);
            }
        })
    });

    $("#logout").click(function(event){
        event.preventDefault();

        $.ajax({
            url: "api/logout",
            method: "GET",
            success: function(data) {
                location.reload();
            },
            error: function(error) {
                console.log(error);
            }
        })
    });
});