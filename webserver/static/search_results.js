
$(document).ready(function(){
    
    $(".country").click(function(){
        route = "/view_country/" + this.id
        window.location.href = route
    })
    $(".city").click(function(){
        route = "/view_city/" + this.id
        window.location.href = route
    })
    $(".continent").click(function(){
        route = "/view_continent/" + this.id
        window.location.href = route
    })
    $( ".card" ).hover(function() {
      $(this).addClass('text-info').css('cursor', 'pointer'); 
    }, function() {
      $(this).removeClass('text-info');
    }
})
