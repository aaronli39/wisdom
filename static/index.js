function suggest() {
    //Variables
    var input, filter, i;
    input = document.getElementById("search_button").value.toUpperCase();
    // input = input.charAt(0).toUpperCase() + input.slice(1);
    console.log(input)
    ctr = 0;
    var schoolData = $("#my-data").attr("data-name");
    schoolData = JSON.parse(schoolData);
    class_names = schoolData["classes"];
    var schoolID = schoolData['schoolID'];
    // console.log(class_names[0]);
    //remove any existing list items
    $("#suggestions").empty();
    //add appropriate list items
    if (class_names.length == 0) {
        $("#suggestions").append("<li>You have no classes, go add one!</li>");
    } 
    for (i = 0; i < class_names.length; i++) {
        if (class_names[i]["className"].includes(input)) {
            var temp = "/school/" + schoolID + "/class/" + class_names[i]["classID"];
            $("#suggestions").append("<a class='btn' href=" + temp + " style='text-align: left; margin-top: 0.2em;' target='_blank'>" + class_names[i]["className"] + " (" + class_names[i]['classID'] + ")</a>");
            ctr++;
        }
        //cut off at 5 list items
        if (ctr == 5) {
            break;
        }
    } if (ctr === 0) {
        $("#suggestions").append("<li style='border: 1px solid lightgray'>Class name not found</li>");
    }
};