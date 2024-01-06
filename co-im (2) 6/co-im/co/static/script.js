document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('.card');

    cards.forEach(function(card) {
        var radios = card.querySelectorAll('input[type="radio"]');

        radios.forEach(function(radio) {
            radio.addEventListener('change', function() {
                card.classList.add('card-checked');
                if (!radio.checked) {
                    card.classList.remove('card-checked');
                }
            });
        });
    });
});
