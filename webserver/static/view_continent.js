
$(document).ready(function(){
    $( ".card" ).hover(function() {
      $(this).addClass('text-info').css('cursor', 'pointer');
    }, function() {
      $(this).removeClass('text-info');
    })
    $(".country").click(function(){
        route = "/view_country/" + this.id
        window.location.href = route
    })
    $(".content").click(function(){
        route = "/view_content/" + this.id
        window.location.href = route
    })
       
})
