$(document).ready(function(){
    var start = null;
    var end = null;
    var price = $("#pricepreview").text();
    
    $("#payments").submit(function(event){
        event.preventDefault();

        if(start != null && end != null){
            var roomid = $("#roomid").val();

            $.ajax({
                url: "api/payment",
                method: "POST",
                data: {start: start.toLocaleDateString("en-US"),end: end.toLocaleDateString("en-US"),roomid: roomid},
                dataType: "json",
                success: function(data) {
                    if(data.code == 200){
                        $("#titlemodal").text("ชำระเงิน")
                        $("#dataresponse").html(data.html);
                    }else{
                        alert(data.message)
                    }
                },
                error: function(error){
                    console.log(error);
                }
            })
        }
    });

    $("#start_book").change(function(e){
        start = new Date($(this).val());
        console.log(start)
        if(start != null && end != null) {
            var diff_new = day_diff(start,end);
            if(diff_new >= 1) {
                sum = price * diff_new;
                $("#priceall").text(sum + " บาท");
            }else{
                alert("กรุณาเลือกวันถัดไป");
                $("#start_book").val(null);
                start = null;
                
            }
        }
    });

    $("#end_book").change(function(e){
        end = new Date($(this).val());
        if(start != null && end != null) {
            var diff_new = day_diff(start,end);
            if(diff_new >= 1) {
                sum = price * diff_new;
                $("#priceall").text(sum + " บาท");
            }else{
                alert("กรุณาเลือกวันถัดไป");
                $("#end_book").val("");
                end = null;
            }
        }
    });
});

function day_diff(start,end) {
    var diff = new Date(end-start);
    return Math.round(diff/1000/60/60/24)
}