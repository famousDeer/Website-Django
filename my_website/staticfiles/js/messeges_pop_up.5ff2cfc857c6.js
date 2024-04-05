var SwalColors = {
    warning: "rgba(177, 195, 45, 0.45)",
    danger: "rgba(209, 36, 36, 0.45)",
    success: "rgba(29, 210, 47, 0.45)"
};

function SwalOverlayColor(color){
    setTimeout(function(){
        $(".swal-overlay").css({"background-color": color});
    }, 10);
}
$(document).ready(function() {
    // Listen event when div shows up
    $('#messege').on('show', function() {
        var messegeId = $(this).attr('id');
        var messageValue = $(this).attr('value');
        SwalOverlayColor(SwalColors["warning"]);
        swal({
            title: "Are you sure?",
            text: "Once deleted, you will not be able to recover this item!",
            icon: "warning",
            dangerMode: true,
        });
    });
});