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