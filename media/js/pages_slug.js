$(function() {
    $("#id_slug").unbind('change');
    $("#id_title").unbind('keyup');

    // Automatically update the slug when typing the title
    var slug_auto = $("#id_title").attr("value") == "";
    var slug = $("#id_slug").change(function() {
        slug_auto && (slug_auto = false);
    });
    $("#id_title").keyup(function() {
        slug_auto && slug.val(URLify(this.value, 64));
    });
});
