require(["jquery", "bootstrap", "moment", "jhapi", "utils"], function(
  $,
  bs,
  moment,
  JHAPI,
  utils
) {
  "use strict";

  var base_url = window.jhdata.base_url;
  var api = new JHAPI(base_url);

  function getGroup(element) {
    var original = element;
    while (!element.hasClass("group-field")) {
      element = element.parent();
      if (element[0].tagName === "BODY") {
        console.error("Couldn't find row for", original);
        throw new Error("No image-row found");
      }
    }
    return element;
  }

  function remove() {
    var el = $(this);
    el.parent().remove();
  }

  $(".add-environment").click(function() {
    var el = $(this);
    var field = getGroup(el);
    var select = $(".environment-select").first().clone();
    var group = field.data('group');
    select.find('select').attr('name', group)
    select.find(".remove-environment").click(remove);
    select.removeClass('hidden');
    select.appendTo(field);
  });

  $(".submit").click(function(e) {
    e.preventDefault();
    var form = $('form');
    var formData = form.serializeArray();
    api.api_request("permissions", {
      type: "POST",
      data: JSON.stringify(formData),
      success: function(reply) {
        window.location.reload();
      },
    });
  });

  $(".remove-environment").click(remove);
});