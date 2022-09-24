console.log('Sanity check!')

// new
// Get Stripe publishable key
fetch("/config/")
.then((result) => {
    return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publickey);

  // new
  // Event handler
$('#buybtn').click(function() {
    // get coin values
    let quantity = $('#id_amount').val()

    // Get Checkout Session ID
    fetch("/create-checkout-session/?" + new URLSearchParams({
    'quantity': quantity
    }))
    .then((result) => {
//    console.log(result);
    return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});
