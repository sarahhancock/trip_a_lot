
$(document).ready(function(){
    
    $(".btn").click(function(){
        
        route = "/view_city/" + this.id
        window.location.href = route
    })
})
