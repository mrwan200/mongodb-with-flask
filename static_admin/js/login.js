$(document).ready(function(){
    $("#logindata").submit(function(event){
        event.preventDefault();

        var username = $("#username").val();
        var password = $("#password").val();

        $.ajax({
            url: "/",
            method: "POST",
            data: {username: username, password: password},
            dataType: "json",
            success: function(data) {
                if(data.code == 200){
                    alert(data.message)
                    location.href = "/dashboard"
                }else{
                    alert(data.message)
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});