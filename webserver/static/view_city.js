
$(document).ready(function(){
    $( ".card" ).hover(function() {
      $(this).addClass('text-info').css('cursor', 'pointer');
    }, function() {
      $(this).removeClass('text-info');
    })    
    $(".content").click(function(){
        route = "/view_content/" + this.id
        window.location.href = route
    })
    $(".country").click(function(){
        route = "/view_country/" + this.id
        window.location.href = route
    })
})
