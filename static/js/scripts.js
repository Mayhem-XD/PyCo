/*!
* Start Bootstrap - Simple Sidebar v6.0.6 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
        // 드롭다운 메뉴 토글 함수
    function toggleDropdown(id) {
        var dropdown = document.getElementById(id);

        // 드롭다운 메뉴의 display 속성을 가져옴
        var dropdownStyle = window.getComputedStyle(dropdown);

        // 드롭다운 메뉴의 display 속성이 "none"이면 보이도록 변경, 그렇지 않으면 숨김 처리
        if (dropdownStyle.display === "none") {
            dropdown.style.display = "block";
        } else {
            dropdown.style.display = "none";
        }
    }

    // 문서 로드 시 모든 드롭다운 메뉴 숨김 처리
    window.onload = function() {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            dropdowns[i].style.display = "none";
        }
    };
    // Datepicker 요소 가져오기
    var datepicker = document.getElementById("datepicker");

    // 주간 Datepicker 설정
    var currentDate = new Date();  // 현재 날짜
    var firstDayOfWeek = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - currentDate.getDay());  // 현재 주의 첫째 날짜
    var lastDayOfWeek = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() + (6 - currentDate.getDay()));  // 현재 주의 마지막 날짜

    // 주간 Datepicker에 대한 옵션 설정
    var options = {
    dateFormat: "yy-mm-dd",  // 날짜 형식
    minDate: firstDayOfWeek,  // 최소 선택 가능한 날짜
    maxDate: lastDayOfWeek,  // 최대 선택 가능한 날짜
    beforeShowDay: function(date) {  // 각 날짜에 대한 스타일 설정
        var cssClass = "";
        if (date >= firstDayOfWeek && date <= lastDayOfWeek) {
        cssClass = "highlight";
        }
        return [true, cssClass];
    },
    onSelect: function(dateText, inst) {  // 날짜 선택 시 이벤트 처리
        // 선택한 날짜 처리
        console.log("선택한 날짜:", dateText);
    }
    };
  
    // Datepicker 초기화
    $(datepicker).datepicker(options);
      });

