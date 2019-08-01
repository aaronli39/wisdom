function suggest() {
    //Variables
    var input, filter, i;
    input = document.getElementById('search_button');
    filter = input.value.toUpperCase();
    //get list of college names
    ctr = 0;
    var college_names = colleges['college_names'];
    //remove any existing list items
    d3.select("#suggestions").selectAll("li").remove();
    //add appropriate list items
    for (i = 0; i < college_names.length; i++) {
        if (college_names[i].toUpperCase().indexOf(filter) > -1) {
            d3.select("#suggestions").insert("li").text(college_names[i]);
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