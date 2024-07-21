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
      // Update the cart items and total
      document.getElementById("cart_items").innerHTML = json.cart_items_html;
      document.getElementById("cart_total").textContent = json.cart_total_html;

      // Reinitialize necessary scripts
      initializePaymentScript();
    },
    error: function (xhr, errmsg, err) {
      console.error(errmsg);
    },
  });
}

function clear_cart() {
  const csrfToken = document.getElementById("csrf_token").value;
  $.ajax({
    type: "POST",
    url: "clear_cart/",
    data: {
      csrfmiddlewaretoken: csrfToken,
      action: "post",
    },
    success: function (json) {
      // Update the cart items and total
      document.getElementById("cart_items").innerHTML = json.cart_items_html;
      document.getElementById("cart_total").textContent = json.cart_total_html;

      // Reinitialize necessary scripts
      initializePaymentScript();
    },
    error: function (xhr, errmsg, err) {
      console.error(errmsg);
    },
  });
}

function initializePaymentScript() {
  const paid = document.getElementById("paid");
  const balance = document.getElementById("balance");
  const total = parseFloat(document.getElementById("cart_total").textContent);

  balance.textContent = `- ${total} XOF`;

  const keypadButtons = document.querySelectorAll(".number-btn");
  keypadButtons.forEach((button) => {
    button.addEventListener("click", () => {
      paid.value += button.value;
      updateBalance();
    });
  });

  function updateBalance() {
    const paidValue = parseFloat(paid.value) || 0;
    const newBalance = paidValue - total;
    balance.textContent = `${newBalance} XOF`;
  }

  paid.addEventListener("input", updateBalance);

  const deleteButton = document.getElementById("clear_btn");
  deleteButton.addEventListener("click", () => {
    paid.value = paid.value.slice(0, -1);
    updateBalance();
  });

  const cancelButton = document.getElementById("cancel_btn");
  cancelButton.addEventListener("click", () => {
    paid.value = "";
    updateBalance();
  });
}

document.addEventListener("DOMContentLoaded", function () {
  initializePaymentScript();
});

document
  .getElementById("submit_form")
  .addEventListener("click", function (event) {
    event.preventDefault();
    document.getElementById("sale_options_form").submit();
  });
