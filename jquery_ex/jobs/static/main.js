function handleUpdate(resp){
    console.log(resp);
    $("#data").html(resp);
}

function handleClick(event){
    console.log("I have been clicked");
    var link=event.target['href'];
    $.get(link).done(handleUpdate);
    event.preventDefault();
}

function main(){
    var links= $("a.joblinks");
    links.click(handleClick);
}
$(main);