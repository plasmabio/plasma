require(["jquery"], function ($) {
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

  function getXSRFToken() {
    const name = "_xsrf=";
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.indexOf(name) === 0) {
        return decodeURIComponent(cookie.substring(name.length, cookie.length));
      }
    }
    return null;
  }

  $(".add-group").click(function () {
    var el = $(this);
    var field = getGroup(el);
    var select = $(".group-select").first().clone();
    var environment = field.data("environment");
    select.find("select").attr("name", environment);
    select.find(".remove-group").click(remove);
    select.removeClass("d-none");
    select.appendTo(field);
  });

  $(".submit").click(function (e) {
    e.preventDefault();
    var form = $("form");
    var formData = form.serializeArray();
    var spinner = $("#saving-permissions-dialog");
    spinner.find(".modal-footer").remove();
    spinner.modal();

    fetch(`/services/tljh_plasma/api/permissions?_xsrf=${getXSRFToken()}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formData),
      credentials: "same-origin"
    })
      .then((response) => {
        if (!response.ok) {
          console.error("Error:", response.error);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

  $(".remove-group").click(remove);
});
