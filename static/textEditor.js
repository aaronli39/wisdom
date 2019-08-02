//This file is used for text editor functionality
//Ctrl + B: Bold text
//Ctrl + U: Underline text
//Ctrl + I: Italicize text

var box, hiddenInput, boxText, submitButton;

var init = function () {
    box = document.getElementById("textEditor");
    hiddenInput = document.getElementById("hiddenInput");
    submitButton = document.getElementById("submitButton");
    document.execCommand("defaultParagraphSeparator", false, "div");
}

var format = function (cmd) {
    console.log(cmd);
    document.execCommand(cmd);
}

init();

box.addEventListener("keydown", function (event) {
    var ctrlDown = event.ctrlKey;
    var keyPressed = event.key.toLowerCase();
    cmd = null;
    if (ctrlDown) {
        switch (keyPressed) {
            case "b": //Check for b pressed
                cmd = "bold";
                break;
            case "i": //Check for i pressed
                cmd = "italic";
                break;
            case "u": //Check for u pressed
                cmd = "underline";
                break;
        }
    }
    format(cmd);
    if (cmd != null) {
        event.preventDefault();
    }

    if (box.innerHTML == null) {
        hiddenInput.value = "No course description.";
    } else {
        hiddenInput.value = box.innerHTML;
    }
});

submitButton.onclick = function () {
    if (box.innerHTML == null) {
        hiddenInput.value = "";
    } else {
        var input = box.innerHTML.trim();
        hiddenInput.value = input;
    }
};
