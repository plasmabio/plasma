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

  $("#build-all").click(function() {
    var buildAll = function(options) {
      return api.api_request("build", options);
    };
    buildAll({
      type: "POST",
      success: function(reply) {
        alert(reply);
      },
    });
  });
});
