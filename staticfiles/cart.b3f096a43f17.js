function update_cart(obj_id, action) {
  const csrfToken = document.getElementById("csrf_token").value;
  $.ajax({
    type: "POST",
    url: `${action}/`,
    data: {
      product_id: obj_id,
      csrfmiddlewaretoken: csrfToken,
      action: "post",
    },
    success: function (json) {
      // Reload the cart content
      $("#cart").load(location.href + " #cart");
    },
    error: function (xhr, errmsg, err) {
      console.error(errmsg);
    },
  });
}

function clear_cart(obj_id) {
  // Retrieve the CSRF token from the hidden input
  const csrfToken = document.getElementById("csrf_token").value;

  $.ajax({
    type: "POST",
    url: "clear_cart/",
    data: {
      product_id: obj_id,
      csrfmiddlewaretoken: csrfToken,
      action: "post",
    },
    success: function (json) {
      console.log(json.cart_total); // Ensure the key matches the JSON response key
      document.getElementById("cart_total").textContent = json.cart_total;
    },
    error: function (xhr, errmsg, err) {
      console.error(errmsg); // Log error message to console
    },
  });
}

