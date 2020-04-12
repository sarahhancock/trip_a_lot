
$(document).ready(function(){
    
    $(".content").click(function(){
        route = "/view_content/" + this.id
        window.location.href = route
    })
    $(".country").click(function(){
        route = "/view_country/" + this.id
        window.location.href = route
    })
})
