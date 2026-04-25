document.addEventListener('DOMContentLoaded', function() {
    const buyButton = document.getElementById('buy-button');

    if (buyButton) {
        buyButton.addEventListener('click', function() {
            const itemId = buyButton.getAttribute('data-item-id');
            const stripeKey = buyButton.getAttribute('data-stripe-key');
            
            const stripe = Stripe(stripeKey);

            buyButton.disabled = true;
            buyButton.innerText = "Ожидание...";

            fetch(`/buy/${itemId}`, { method: 'GET' })
            .then(response => response.json())
            .then(session => {
                if (session.error) {
                    alert(session.error);
                    buyButton.disabled = false;
                    buyButton.innerText = "Купить";
                } else {
                    return stripe.redirectToCheckout({ sessionId: session.session_id });
                }
            })
            .catch(error => {
                console.error("Error:", error);
                buyButton.disabled = false;
                buyButton.innerText = "Купить";
            });
        });
    }
});