function addResult(city) {
    var city_name = city["name"]

    var card_container = $("<div class = 'card_container'>")

    var card = $("<div class='card'>")
    card.attr('id', city_name)


    var body = $("<div class='card-body'>")
    var title = $("<h5 class='card-title'>")
    title.append(city_name)

    body.append(title)
    card.append(body)
    card_container.append(card)
    $("#results").append(card_container)
}

$(document).ready(function(){
    for city in cities:
        addResult(city)
})
