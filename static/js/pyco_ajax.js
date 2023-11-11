// ###################### open_api ##########################
function send_val() {
    let timep = $('#timep').val();
    let stn = $('#input_stn').val()
    $.ajax({
        type: 'POST',
        url: '/api/stn_rt_location' ,      // 주소 추가해야함
        data: { timep: timep, stn: stn},
        success: function (result) {
            $('#init_img').css('display', 'none');      // 기존 이미지 숨김
            $('#show_img').css('display', 'block');     // 이미지 보여 줄 곳
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
        url: '/api/stn_rt_location',
        data: { place: place},
        success: function (show) {
            $('#imageInput').attr('class','mt-2');
            $('#showmap').attr({ "src": "{{url_for('static',filename='img/rtstn.html')}}" });
        }
    });
}
// ################################################################
// ##################### crawling #################################
function ss_search() {
    let place = $('#place').val();
    $.ajax({
        type: 'POST',
        url: '/crawling/siksin' ,
        data: { place : place},
        success: function (result) {
            $('#siksinTable').css('display', 'block'); 
            let table = $(".siksinTable");
        for (let i = 0; i < result.length; i++) {
            let siksin = result[i];
            let row = "<tr>" +
                "<td><img src='" + siksin.img + "' height='50px'></td>" +
                "<td>" + siksin.title + "</td>" +
                "<td>" + siksin.score + "</td>" +
                "<td>" + siksin.location + "</td>" +
                "<td>" + siksin.menu + "</td>" +
                "</tr>";
            table.append(row);
        }
        }
    });
}

// ##################################################################