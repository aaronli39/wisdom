function suggest2() {
    //Variables
    var input, filter, i;
    var classes, temp;
    input = document.getElementById("search_button2").value.toLowerCase();
    ctr = 0;
    var schoolData = $("#sData").attr("data-name");
    schoolData = JSON.parse(schoolData);
    student_names = schoolData["students"];
    // console.log(student_names[0]["name"]);
    // var schoolID = schoolData['schoolID'];
    // console.log(student_names[0]);
    //remove any existing list items
    $("#suggestions2").empty();
    //add appropriate list items
    if (student_names.length == 0) {
        $("#suggestions2").append("<li>You have no students, go add one!</li>");
    } 
    for (i = 0; i < student_names.length; i++) {
        // console.log(student_names.length);
        temp = student_names[i]["name"][1].toLowerCase() + ", " + student_names[i]["name"][0].toLowerCase();
        if (temp.indexOf(input) > -1) {
            $("#suggestions2").append("<li class='b2'>" + student_names[i]["name"][1] + ", " + student_names[i]["name"][0] + "</li>");
            ctr++;
        }
        //cut off at 5 list items
        if (ctr == 5) {
            break;
        }
    }
    //when user clicks a list item, change the search field to that item
    var clist = document.getElementsByClassName("b2");
    // console.log(clist);
    for (i = 0; i < clist.length; i++) {
        clist[i].addEventListener('click', function (e) {
            // console.log(document.getElementById("search_button").value);
            // $("suggestions").value
            $("#suggestions2").empty();
            for (i = 0; i < student_names.length; i++) {
                temp = this.innerHTML.split(", ");
                console.log(temp);
                var x;
                for (x = 0; x < student_names.length; x++) {
                    if (temp[0] == student_names[x]["name"][1] && temp[1] == student_names[x]["name"][0]) {
                        console.log(student_names[x]["name"][0] == temp[1]);
                        // $("#classList").value = student_names[x]["name"]
                    }
                }
            }
            document.getElementById("search_button2").value = this.innerHTML;
        });
    }
};