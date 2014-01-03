$(document).ready(function() {
    $("#registerButton").button();
    $("#registerButton").click(function() {
        $("#registerButton").button('loading');
    });
});