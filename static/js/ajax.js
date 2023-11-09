function changeQuote(){
    $.ajax({
        type: 'GET',
        url: '/change_quote',
        data: ' ',                           // 서버로 전달할 데이터
        success: function(msg){             // msg: 서버로부터 받은 데이터
            $('#quoteMsg').html(msg);
        }
    });
}
function change_addr(){
    $('#addrInput').attr('class','mt-2');           // input box가 보이게
}
function addrSubmit(){
    $('#addrInput').attr('class','mt-2 d-none');       // input box 안보이게
    let addr = $('#addrInputTag').val();
    $.ajax({
        type: 'GET',
        url: '/change_addr',
        data: {addr:addr},
        success: function(msg){
            $('#addr').html(msg);
        }

    });
}
function changWeather(){
    let addr = $('#addr').text();           // 서버로 부터 받은 데이터
    $.ajax({
        type: 'GET',
        url: '/change_weather',
        data: {addr:addr},
        success: function(result){          // 성공시 실행
            $('#weather').html(result);     // 날씨 전달
        }
    });

}
function changeProfile(){
    $('#imageInput').attr('class','mt-2');      // hidden 상태의 img tag을 보여줌
}
function imageSubmit(){
    let imageInputValue = $('#image')[0];
    let formData = new FormData();
    formData.append('image',imageInputValue.files[0]);
    $.ajax({
        type: 'POST',
        url: '/change_profile',             // formData로
        data: formData,
        processData: false,     // jQuery가 데이터를 쿼리 문자열로 변환하는 것을 방지 formData는 이미 적절한 형식
        contentType: false,     //  jQuery가 Content-Type 헤더를 설정하는 것을 방지 formData를 사용할 때는 브라우저가 적절한 Content-Type을 설정
        success: function(result){
            $('#imageInput').attr('class','mt-2 d-none');           // img tag를 숨김
            fname = 'http://127.0.0.1:5000/static/data/profile.png?q=' + result;
            $('#profile').attr('src',fname);
        }
    });
}
function showHotplaces(){
    $('#resDiv').attr('class','mt-2')   // hidden 속성 제거
}