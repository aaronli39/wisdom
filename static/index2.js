function suggest2() {
    //Variables
    var input, i;
    var temp;
    ctr = 0;
    input = document.getElementById("search_button2").value.toLowerCase();
    var schoolData = $("#sData").attr("data-name");
    schoolData = JSON.parse(schoolData);
    student_names = schoolData["students"];

    //remove any existing list items
    $("#suggestions2").empty();
    $("#classList").empty();
    //add appropriate list items
    if (student_names.length === 0) {
        $("#suggestions2").append("<li>You have no students, go add one!</li>");
    }
    for (i = 0; i < student_names.length; i++) {
        console.log("entered")
        temp = student_names[i]["name"][1].toLowerCase() + student_names[i]["name"][0].toLowerCase() + student_names[i]['studentID'];
        if (temp.includes(input)) {
            $("#suggestions2").append(`<li class='b2'> ${student_names[i]["name"][1]}, ${student_names[i]["name"][0]} (${student_names[i]['studentID']})</li>`);
            ctr++;
        }
        //cut off at 5 list items
        if (ctr === 5) {
            break;
        }
    } if (ctr === 0) $("#suggestions2").append("<li>No results</li>");
    var z;
    document.getElementById("suggestions2").addEventListener('click', function (e) {
        $("#classList").empty();
        $("#classList").append("<li style='text-decoration: underline; border: none; padding-left: 0;'>Classes:</li>");
        for (i = 0; i < student_names.length; i++) {
            temp = e.target.innerText
            console.log(temp)
            temp = temp.slice(0, temp.indexOf(" (")).split(", ")
            var x;
            for (x = 0; x < student_names.length; x++) {
                if (temp[0] === student_names[x]["name"][1] && temp[1] === student_names[x]["name"][0]) {
                    if (student_names[x]["classes"].length === 0) {
                        // document.getElementById("suggestions2").style.display = "none"
                        $("#classList").append("<li>This student has no classes</li>");
                        return;
                    } else {
                        for (z = 0; z < student_names[x]["classes"].length; z++) {
                            console.log(student_names[x]["classes"][z])
                            $("#classList").append(`<li> ${student_names[x]["classes"][z][1]}: (${student_names[x]["classes"][z][0]}) </li>`);
                            return;
                        }
                    }
                }
            }
        }
    });
    document.getElementById("suggestions2").style.display = "list-item"
};