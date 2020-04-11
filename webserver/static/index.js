
$(document).ready(function(){
    alert("hi!")
    $(".card").click(function(){
        alert(this.id)
        route = "/view/" + this.id
        window.location.href = route
    })
})
