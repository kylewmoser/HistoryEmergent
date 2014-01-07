$(document).ready(function() {
    $("#signinButton").button();
    $("#signinButton").click(function() {
        $("#signinButton").button('loading');
    });
});