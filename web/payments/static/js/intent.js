document.addEventListener('DOMContentLoaded', async function() {
    const form = document.getElementById('payment-form');
    if (!form) return;

    const itemId = form.getAttribute('data-item-id');
    const stripeKey = form.getAttribute('data-stripe-key');
    const stripe = Stripe(stripeKey);
    
    const elements = stripe.elements();
    const cardElement = elements.create('card');
    cardElement.mount('#card-element');

    const submitBtn = document.getElementById('submit-button');
    const messageDiv = document.getElementById('payment-message');

    const response = await fetch(`/intent/${itemId}/`);
    const data = await response.json();
    const clientSecret = data.client_secret;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        submitBtn.disabled = true;
        submitBtn.innerText = "Ожидание";

        const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardElement,
            }
        });

        if (error) {
            messageDiv.classList.remove('hidden');
            messageDiv.innerText = error.message;
            submitBtn.disabled = false;
            submitBtn.innerText = "Оплатить";
        } else if (paymentIntent && paymentIntent.status === 'succeeded') {
            form.innerHTML = "<h3 style='color: green;'>Оплата прошла успешно!</h3>";
            setTimeout(() => { window.location.href = "/"; }, 3000);
        }
    });
});