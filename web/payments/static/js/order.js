document.addEventListener('DOMContentLoaded', function() {
    const buyOrderBtn = document.getElementById('buy-order-button');

    if (buyOrderBtn) {
        buyOrderBtn.addEventListener('click', function() {
            const orderId = buyOrderBtn.getAttribute('data-order-id');
            const stripeKey = buyOrderBtn.getAttribute('data-stripe-key');
            const stripe = Stripe(stripeKey);

            buyOrderBtn.disabled = true;
            buyOrderBtn.innerText = "Ожидание...";

            fetch(`/buy_order/${orderId}/`, { method: 'GET' })
            .then(response => response.json())
            .then(session => {
                if (session.error) {
                    alert(session.error);
                    buyOrderBtn.disabled = false;
                    buyOrderBtn.innerText = "Оплатить заказ";
                } else {
                    return stripe.redirectToCheckout({ sessionId: session.session_id });
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
});