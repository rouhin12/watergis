var open = false;
let selected = false;

$("#closeNavContent").click(function () {
    $(".navContent").removeClass("open");
    $(".menuItem").removeClass("active");
    open = false;
});

function showContent(id) {
    if (!open) {
        $(".navContent").addClass("open");
        open = true;
        $(".subContent").removeClass("d-block");
        $("#" + id + ".subContent").addClass("d-block");
        $(".menuItem").removeClass("active");
        $("#" + id + "CTA").addClass("active");
    } else {
        $(".subContent").removeClass("d-block");
        $("#" + id + ".subContent").addClass("d-block");
        $(".menuItem").removeClass("active");
        $("#" + id + "CTA").addClass("active");
    }
}