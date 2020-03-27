require(["jquery", "bootstrap", "moment", "jhapi", "utils"], function(
  $,
  bs,
  moment,
  JHAPI,
  utils
) {
  "use strict";

  var base_url = '/services/images';
  var api = new JHAPI(base_url);

  var build = function(options) {
    return api.api_request("build", options);
  };

  $("#add-image").click(function() {
    var dialog = $("#add-image-dialog");
    dialog.modal();
  });

  $("#add-image-dialog")
    .find(".save-button")
    .click(function() {
      var dialog = $("#add-image-dialog");
      var repo = dialog.find(".repo-input").val();
      var ref = dialog.find(".ref-input").val();
      console.log(repo, ref);
      build({
        type: "POST",
        data: JSON.stringify({
          repo: repo,
          ref: ref
        }),
        dataType: null,
        success: function(reply) {
          console.log(reply)
          window.location.reload();
        },
      });
    });
});
