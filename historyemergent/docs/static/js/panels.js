$(document).ready(function() {
    var animateSpeed = 275;
    // Panel Visibility
    $("#showPanel").hide();
    $("#hideButton").click(function() {
        $("#actionPanel").slideUp(animateSpeed);
        $("#editForm").slideUp(animateSpeed);
        $("#fileForm").slideUp(animateSpeed);
        $("#showPanel").slideDown(animateSpeed);
    });
    $("#showButton").click(function() {
        $("#actionPanel").slideDown(animateSpeed);
        $("#showPanel").slideUp(animateSpeed);
    })

    // title form
    $("#editForm").hide();
    $("#editButton").click(function() {
        $("#editForm").slideDown(animateSpeed);
    });
    $("#hideFormButton").click(function() {
        $("#editForm").slideUp(animateSpeed);
    })


    // file form
    $("#fileForm").hide();
    $("#fileFormButton").click(function() {
        $("#fileForm").slideDown(animateSpeed);
    });
    $("#hideFileFormButton").click(function() {
        $("#fileForm").slideUp(animateSpeed);
    })
});