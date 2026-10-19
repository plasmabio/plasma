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

  // The submit button is only enabled when the form differs from the last
  // saved state, and the status next to it tells what happened.
  var saving = false;
  var savedState;
  $(function () {
    savedState = serializeForm();
  });

  function serializeForm() {
    return JSON.stringify(
      $("form")
        .serializeArray()
        .map(function (arg) {
          return arg.name + "=" + arg.value;
        })
        .sort()
    );
  }

  function setStatus(text, className) {
    $(".submit-status")
      .text(text)
      .removeClass("text-success text-danger text-warning")
      .addClass(className || "");
  }

  function refresh() {
    if (saving) {
      return;
    }
    var dirty = serializeForm() !== savedState;
    $(".submit").prop("disabled", !dirty);
    if (dirty) {
      setStatus("Unsaved changes", "text-warning");
    } else if ($(".submit-status").hasClass("text-warning")) {
      setStatus("");
    }
  }

  function remove() {
    var el = $(this);
    el.parent().remove();
    refresh();
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
    refresh();
  });

  $("form").on("change", "select", refresh);

  $(".submit").click(function (e) {
    e.preventDefault();
    var button = $(this);
    var formData = $("form").serializeArray();
    var submittedState = serializeForm();
    saving = true;
    button.prop("disabled", true);
    setStatus("Saving…");

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
          throw new Error(`${response.status} ${response.statusText}`);
        }
        savedState = submittedState;
        return ["Permissions saved", "text-success"];
      })
      .catch((error) => {
        console.error("Error:", error);
        return ["Saving failed: " + error.message, "text-danger"];
      })
      .then(([text, className]) => {
        saving = false;
        refresh();
        setStatus(text, className);
      });
  });

  $(".remove-group").click(remove);

  $("#env-filter").on("input", function () {
    var query = $(this).val().toLowerCase();
    $(".group-field").each(function () {
      var name = $(this).find("legend a").text().toLowerCase();
      var owner = $(this).find(".env-owner").text().toLowerCase();
      $(this).toggle(name.includes(query) || owner.includes(query));
    });
  });
});
