
$(document).ready(function(){
    
    $(".btn").click(function(){
        
        route = "/view/" + this.id
        window.location.href = route
    })
})
