require(["jquery", "bootstrap", "moment", "jhapi", "utils"], function(
  $,
  bs,
  moment,
  JHAPI,
  utils
) {
  "use strict";

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

});