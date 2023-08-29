const stripePublicKey = document.getElementById('id_stripe_public_key').innerText.slice(1, -1);
const clientSecret = document.getElementById('id_client_secret').innerText.slice(1, -1);
const stripe = Stripe(stripePublicKey);

const style = {
  base: {
      fontSize: '16px',
  },
  invalid: {
      color: '#dc3545',
      iconColor: '#dc3545'
  }
};
const elements = stripe.elements({ clientSecret });
const card = elements.create('card', {style: style});
card.mount('#card-element');

//Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
  let errorDiv = document.getElementById('card-errors');
  if (event.error) {
    let html = `
        <span class="icon" role="alert">
            <i class="fa-regular fa-circle-xmark"></i>
        </span>
        <span>${event.error.message}</span>
    `;
    errorDiv.innerHTML = html;
  } else {
      errorDiv.innerText = '';
  }
});

// Handle payment form submit
const form = document.getElementById('payment-form');

form.addEventListener('submit', function(event) {
  event.preventDefault();

  card.update({'disabled': true});
  document.getElementById('submit-button').setAttribute('disabled', true);

  stripe.confirmCardPayment(clientSecret, {
      payment_method: {
          card: card,
      }
  }).then(function(result) {
      if (result.error) {
          let errorDiv = document.getElementById('card-errors');
          let html = `
              <span class="icon" role="alert">
              <i class="fas fa-times"></i>
              </span>
              <span>${result.error.message}</span>`;
          errorDiv.innerHTML(html);
          card.update({ 'disabled': false});
          document.getElementById('submit-button').setAttribute('disabled', false);
      } else {
          if (result.paymentIntent.status === 'succeeded') {
              form.submit();
          }
      }
  });
});