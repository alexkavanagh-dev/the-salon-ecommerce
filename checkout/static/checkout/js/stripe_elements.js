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
  document.getElementById('loading-overlay').classList.remove('d-none');
  document.getElementById('loading-spinner').classList.remove('d-none');

  let saveInfo = Boolean($('#id-save-info').attr('checked'));
  // From using {% csrf_token %} in the form
  let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  let postData = {
    'csrfmiddlewaretoken': csrfToken,
    'client_secret': clientSecret,
    'save_info': saveInfo,
  };
  let url = '/checkout/cache_checkout_data/';

  $.post(url, postData).done(function () {
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: card,
          billing_details: {
              name: form.full_name.value.trim(),
              phone: form.phone_number.value.trim(),
              email: form.email.value.trim(),
              address:{
                  line1: form.street_address1.value.trim(),
                  line2: form.street_address2.value.trim(),
                  city: form.town_or_city.value.trim(),
                  state: form.county.value.trim(),
              }
          }
      },
      shipping: {
          name: form.full_name.value.trim(),
          phone: form.phone_number.value.trim(),
          address: {
              line1: form.street_address1.value.trim(),
              line2: form.street_address2.value.trim(),
              city: form.town_or_city.value.trim(),
              postal_code: form.postcode.value.trim(),
              state: form.county.value.trim(),
          }
      },
    }).then(function(result) {
        if (result.error) {
            let errorDiv = document.getElementById('card-errors');
            let html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            errorDiv.innerHTML(html);
            document.getElementById('loading-overlay').classList.add('d-none');
            document.getElementById('loading-spinner').classList.add('d-none');
            card.update({ 'disabled': false});
            document.getElementById('submit-button').setAttribute('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
      });
  }).fail(function () {
    // just reload the page, the error will be in django messages
    location.reload();
  })
});
