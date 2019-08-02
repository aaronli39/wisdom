function suggest() {
    //Variables
    var input, filter, i;
    input = document.getElementById("search_button").value;
    input = input.charAt(0).toUpperCase() + input.slice(1);
    ctr = 0;
    var schoolData = $("#my-data").attr("data-name");
    schoolData = JSON.parse(schoolData);
    console.log(schoolData);
    class_names = schoolData["classes"];
    var schoolID = schoolData['schoolID'];
    // console.log(class_names[0]);
    //remove any existing list items
    $("#suggestions").empty();
    //add appropriate list items
    if (class_names.length == 0) {
        $("#suggestions").append("<li>You have no classes, go add one!</li>");
    } 
    console.log(class_names[0]);
    for (i = 0; i < class_names.length; i++) {
        // console.log(class_names.length);
        if ((class_names[i]["className"].charAt(0).toUpperCase() + class_names[i]["className"].slice(1)).indexOf(input) > -1) {
            var temp = "/school/" + schoolID + "/class/" + class_names[i]["classID"];
            $("#suggestions").append("<a class='btn' href=" + temp + " style='text-align: left; margin-top: 0.2em;'>" + class_names[i]["className"] + " (" + class_names[i]['classID'] + ")</a>");
            ctr++;
        }
        //cut off at 5 list items
        if (ctr == 5) {
            break;
        }
    }
    //when user clicks a list item, change the search field to that item
    var clist = document.getElementsByTagName("li");
    // console.log(clist);
    for (i = 0; i < clist.length; i++) {
        clist[i].addEventListener('click', function (e) {
            // console.log(document.getElementById("search_button").value);
            // $("suggestions").value
            document.getElementById("search_button").value = this.innerHTML;
        });
    }
};