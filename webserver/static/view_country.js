
$(document).ready(function(){
    
    $(".city").click(function(){
        route = "/view_city/" + this.id
        window.location.href = route
    })
    $(".content").click(function(){
        route = "/view_content/" + this.id
        window.location.href = route
    })
})
