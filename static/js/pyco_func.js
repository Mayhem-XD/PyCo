// ############## user #####################
function updateEmail() {
    var emailInput = document.querySelector('#email');
    var emailSelect = document.querySelector('#emailDomain');
    emailInput.value = emailInput.value.split('@')[0] + emailSelect.value;
}
// #################################################

// ################### board ############################
function search() {
    const field = $('#field').val();
    const query = $('#query').val();
    location.href = "/board/list?p={{session['current_page']}}&f=" + field + '&q=' + query;
}
// ######################################################

// ################################# python func ##########################################
$(document).ready(function() {
    $('#example').DataTable({
        info: false,
        searching: true,
        paging: true,
        ordering: false,
        //order: [[ 0, "asc" ]],
        columnDefs: [{
            "targets": [ 0 ],
            "visible": false,
            "searchable": false
        }],
        language: {
            thousands: ',',
            search: '',
            searchPlaceholder: "검색어",
            paginate: {
                first: '처음',
                previous: '이전',
                next: '다음',
                last: '마지막',
            }
        },
        oLanguage: {
            sLengthMenu: "_MENU_",
        },
        "lengthMenu": [[10, -1], ["10개씩 보기", "모두 보기"]]
    });
} );
// ############################################################################