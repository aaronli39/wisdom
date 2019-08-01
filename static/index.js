function suggest() {
    //Variables
    var input, filter, i;
    input = document.getElementById("search_button").value;
    input = input.charAt(0).toUpperCase() + input.slice(1);
    ctr = 0;
    var class_names = document.getElementById("my-data").data;
    console.log(class_names);
    //remove any existing list items
    $("#suggestions").empty();
    //add appropriate list items
    if (class_names.length == 0) {
        $("#suggestions").append("<li>You have no classes, go add one!</li>");
    } for (i = 0; i < class_names.length; i++) {
        if (class_names[i].toUpperCase().indexOf(filter) > -1) {
            d3.select("#suggestions").insert("li").text(class_names[i]);
            ctr++;
        }
        //cut off at 5 list items
        if (ctr == 5) {
            break;
        }
    }
    
    //when user clicks a list item, change the search field to that item
    var clist = document.getElementsByTagName("li");
    for (i = 1; i < clist.length; i++) {
        clist[i].addEventListener('click', function () {
            console.log(this);
            input.value = this.innerText;
        });
    }
};