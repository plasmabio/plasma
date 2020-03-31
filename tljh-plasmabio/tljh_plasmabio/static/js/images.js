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

  function getRow(element) {
    var original = element;
    while (!element.hasClass("image-row")) {
      element = element.parent();
      if (element[0].tagName === "BODY") {
        console.error("Couldn't find row for", original);
        throw new Error("No image-row found");
      }
    }
    return element;
  }

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
      api.api_request("build", {
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

  $(".remove-image").click(function() {
    var el = $(this);
    var row = getRow(el);
    var image = row.data("image");
    var dialog = $("#remove-image-dialog");
    dialog.find(".delete-image").text(image);
    dialog.modal();
  });

  $("#remove-image-dialog")
    .find(".remove-button")
    .click(function() {
      var dialog = $("#remove-image-dialog");
      var image = dialog.find(".delete-image").text();
      $("#removing-image-dialog").modal();
      api.api_request("build", {
        type: "DELETE",
        data: JSON.stringify({
          name: image
        }),
        dataType: null,
        success: function(reply) {
          window.location.reload();
        },
      })
    });
});
