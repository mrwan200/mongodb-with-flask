$(document).ready(function(){
    $("#showslipt").click(function(event){
        event.preventDefault();
        var sliptid = $(this).data("splitid");

        $("#loadimages").attr("src",window.location.origin + "/images/" + sliptid)
        $("#show_images").modal("show")
    });

    $("#confrim, #confrim").click(function(event){
        event.preventDefault();
        var status_payment = $(this).data("status")
        var uuid_booking = $(this).data("splitid")

        if(status_payment == true){
            status = "ยืนยันการชำระเงิน";
        }else if(status_payment == false){
            status = "ไม่ยืนยันการชำระเงิน และ ลบข้อมูลการจองหัองพัก";
        }
        
        $("#confrim_send").attr("data-uuid",uuid_booking);
        $("#confrim_send").attr("data-status",status_payment);
        $("#showconfrim").text("คุณแน่ใจหรือไม่ว่า ต้องการ" + status + " หรือไม่")
        $("#confrim_show").modal("show");
    });

    $("#confrim_send").click(function(event){
        event.preventDefault();

        var uuid_booking = $(this).data("uuid")
        var status_payment = $(this).data("status")
        $.ajax({
            url: "/payments",
            method: "POST",
            data: {uuid: uuid_booking, status: status_payment},
            dataType: "json",
            success: function(data) {
                if(data.code == 200){
                    alert(data.message);
                    location.reload()
                }else{
                    alert(data.message);
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    

    $("#logout").click(function(event){
        event.preventDefault();

        $.ajax({
            url: "/logout",
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