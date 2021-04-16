(function () {
    // get select element
    select_variacao = document.getElementById('select-variacoes');

    // get precos *those who are already being showed*
    variation_preco = document.getElementById('variation-preco');
    variation_preco_promocional = document.getElementById('variation-preco-promocional');

    // return if select_variacao not 've clicked yet
    if (!select_variacao) {
        return;
    }

    // return if variacao_preco is absent
    if (!variation_preco) {
        return;
    }

    // add event listener 4 change precos, based on those from variacao
    select_variacao.addEventListener('change', function () {

        //  get variacao precos from select options 
        preco = this.options[this.selectedIndex].getAttribute('data-preco');
        preco_promocional = this.options[this.selectedIndex].getAttribute('data-preco-promocional');

        // set values
        if (variation_preco && preco) {
            variation_preco.innerHTML = preco;
        }
        
        if (variation_preco_promocional && preco_promocional) {
            variation_preco_promocional
        
        } else {
            variation_preco_promocional = preco;
            variation_preco.innerHTML = '';
 
        }

    })
})();

