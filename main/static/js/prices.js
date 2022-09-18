const coins = {
    'BTC': 609,
    'ETH': 103,
    'LTC': 54,
    'EOS': 94,
    'KINGM': 66,
    'XRP': 14,
    'ADA': 44,
    'DOGE': 21,
    'SHIB': 24
};

$('select[name="product"]').change(function () {
    if(this.value in coins) {
        let price = parseInt($('#id_amount').val())
        if (Number(price)) {
            $('#amount').val(price / coins[this.value])
        } else {
            console.log('Not a number')
        }
    }
});

$('#id_amount').keyup(function () {
    let coin = $('select[name="product"] option:selected').val();
    if(coin in coins) {
        let price = parseInt(this.value)
        if (Number(price)) {
            $('#amount').val(price / coins[coin])
        } else {
            console.log('here')
        }
    }
});
