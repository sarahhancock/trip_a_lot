
$(document).ready(function(){
    
    $(".city").click(function(){
        route = "/view_content/" + this.id
        window.location.href = route
    })
})
