
$(document).ready(function(){
    
    $(".country").click(function(){
        route = "/view_country/" + this.id
        window.location.href = route
    })
    $(".city").click(function(){
        route = "/view_city/" + this.id
        window.location.href = route
    })
})
