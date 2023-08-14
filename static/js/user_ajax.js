// JavaScript (jQuery)
$(document).ready(function() {
    $("#uid").on("change",function() {
        let uid = $('#uid').val();
        $.ajax({
            url: "/user/checkUid",
            type: "GET",
            data: { uid: uid },
            success: function(data) {
                $("#uidCheckMsg").text(data);
            }
        });
    });
    
    $("#pwd2").on("change",function() {
        let pwd = $("#pwd").val();
        let pwd2 = $("#pwd2").val();
        if(pwd !== pwd2) {
            $("#pwd").css("background-color", "#ffc1cc");
            $("#pwd2").css("background-color", "#ffc1cc");
        } else {
            $("#pwd").css("background-color", "#ccff00");
            $("#pwd2").css("background-color", "#ccff00");
        }
    });
    
    
    
    
});