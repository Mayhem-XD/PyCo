function send_val() {
    let timep = $('#timep').val();
    let stn = $('#input_stn').val()
    $.ajax({
        type: 'POST',
        url: '/' ,      // 주소 추가해야함
        data: { timep: timep, stn: stn},
        success: function (result) {
            $('#init_img').css('display', 'none');
            $('#show_img').css('display', 'block');
            let dn = result.dn;
            let up = result.up;
            $('#i1').attr('src', '/static/img/stage_'+dn+'.png');
            $('#i2').attr('src', '/static/img/stage_'+up+'.png');

        }

    });
}

function getStnInfo() {
    let palce = $('#input_line').val();
    $.ajax({
        type: 'POST',
        url: '/stn_rt_location',
        data: { place: place},
        success: function (show) {
            $('#imageInput').attr('class','mt-2');
            $('#showmap').attr({ "src": "{{url_for('static',filename='img/rtstn.html')}}" });
        }
    });
}