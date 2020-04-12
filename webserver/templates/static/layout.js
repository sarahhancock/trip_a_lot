var search_for = function(search_term){
    window.location.href = "/search?q=" + search_term
}

$(document).ready(function(){
    $("#search-btn").click(function(){
        search_for($("#search-inp").val());
        
    })
    $("#search-inp").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#search-btn").click();
    }
});
})
