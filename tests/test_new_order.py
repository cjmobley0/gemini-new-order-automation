import pytest
from src.order_placement_apis.new_order import NewOrder
from utils.get_crypto_price import get_crypto_price


@pytest.fixture()
def new_order():
    return NewOrder(symbol='btcusd',
                    amount='1',
                    price='5',
                    side='buy',
                    type='exchange limit')


@pytest.fixture()
def get_eth_price():
    return get_crypto_price('ETHUSD')


@pytest.fixture()
def get_btc_price():
    return get_crypto_price('BTCUSD')

#############################################
#                                           #
#       Positive Happy Path TCs:            #
#                                           #
#############################################


@pytest.mark.positive
def test_new_order_post_200(new_order):
    """ Verify New Order POST request returns 200 status """
    assert new_order.new_order_post().status_code == 200


@pytest.mark.positive
@pytest.mark.parametrize("field, expected_type", [
    ("order_id", str),
    ("id", str),
    ("symbol", str),
    ("exchange", str),
    ("avg_execution_price", str),
    ("side", str),
    ("type", str),
    ("timestamp", str),
    ("timestampms", int),
    ("is_live", bool),
    ("is_cancelled", bool),
    ("is_hidden", bool),
    ("was_forced", bool),
    ("executed_amount", str),
    ("options", list),
    ("price", str),
    ("original_amount", str),
    ("remaining_amount", str)
])
def test_new_order_fields_and_types(new_order, field, expected_type):
    """ Verify New Order POST request returns a JSON when using the following fields and types """
    response = new_order.new_order_post()

    assert type(response.json().get(field)) is expected_type


@pytest.mark.positive
def test_new_order_nonce_matches_timestamp(new_order):
    """ Verify New Order POST request nonce value matches the JSON response timestamp value """
    response = new_order.new_order_post()

    # Cutting timestamp off by one digit due to flakyness of this test where the milliseconds in travel time
    # causes one point differences between the 2 values
    assert new_order.nonce[:-5] == response.json().get('timestamp')[:-2]


@pytest.mark.positive
@pytest.mark.parametrize("symbol", ["btcusd", "ethusd", ])
def test_new_order_symbol_matches(symbol):
    """
        Verify New Order POST request symbol value matches the JSON response symbol value
        btcusd
        ethusd
    """
    new_order = NewOrder(symbol=symbol,
                         amount='1',
                         price='5',
                         side='buy',
                         type='exchange limit')
    response = new_order.new_order_post()

    assert response.json().get('symbol') == symbol


@pytest.mark.positive
@pytest.mark.parametrize("amount", ["1", "0.4"])
def test_new_order_amount_matches(amount):
    """
        Verify New Order POST request amount value matches the JSON response original_amount value
            1
            0.4
    """
    new_order = NewOrder(symbol='btcusd',
                         amount=amount,
                         price='5',
                         side='buy',
                         type='exchange limit')
    response = new_order.new_order_post()

    assert response.json().get('original_amount') == amount


@pytest.mark.positive
@pytest.mark.parametrize("price, expected_price", [("100", "100.00"), ("10.5", "10.50")])
def test_new_order_price_matches(price, expected_price):
    """
        Verify New Order POST request price value matches the JSON response price value
            100
            10.0
    """
    new_order = NewOrder(symbol='btcusd',
                         amount='1',
                         price=price,
                         side='buy',
                         type='exchange limit')
    response = new_order.new_order_post()

    assert response.json().get('price') == expected_price


@pytest.mark.positive
@pytest.mark.parametrize("side", ["buy", "sell"])
def test_new_order_side_matches(side):
    """
        Verify New Order POST request side value matches the JSON response side value
            buy
            sell
    """
    new_order = NewOrder(symbol='btcusd',
                         amount='1',
                         price='5',
                         side=side,
                         type='exchange limit')
    response = new_order.new_order_post()

    assert response.json().get('side') == side


@pytest.mark.positive
@pytest.mark.parametrize("type, expected_type", [
    ("exchange limit", "exchange limit"),
    ("exchange stop limit", "stop-limit")
])
def test_new_order_type_matches(type, expected_type):
    """
        Verify New Order POST request type value matches the JSON response type value
            exchange limit: exchange limit
            exchange stop limit: stop-limit
    """
    new_order = NewOrder(symbol='btcusd',
                         amount='1.2',
                         price='70500',
                         side='buy',
                         type=type,
                         stop_price='70000')
    response = new_order.new_order_post()

    assert response.json().get('type') == expected_type


######################################################
#                                                    #
#       Positive Optional Parameters TCs:            #
#                                                    #
######################################################


@pytest.mark.positive
def test_new_order_client_order_id_matches():
    """
        Verify New Order POST request client_order_id value matches the JSON response client_order_id value
    """
    expected_id = 'cm-111521'
    new_order = NewOrder(symbol='btcusd',
                         amount='1',
                         price='5',
                         side='buy',
                         type='exchange limit',
                         client_order_id=expected_id)
    response = new_order.new_order_post()
    assert response.json().get('client_order_id') == expected_id


@pytest.mark.positive
@pytest.mark.parametrize("side, price, stop_price", [
    ("buy", "70500", "70000")
])
def test_new_order_client_order_id_matches(side, price, stop_price):
    """
        Verify New Order POST request stop_price value for buy and sell returns 200 response
    """
    new_order = NewOrder(symbol='btcusd',
                         amount='1.2',
                         price=price,
                         side=side,
                         type='exchange stop limit',
                         stop_price=stop_price)
    new_order.new_order_post()
    assert new_order.status_code == 200


@pytest.mark.positive
def test_new_order_account_matches():
    """
        Verify New Order POST request client_order_id value matches the JSON response client_order_id value
    """
    new_order = NewOrder(symbol='btcusd',
                         amount='1',
                         price='5',
                         side='buy',
                         type='exchange limit',
                         account='cm-test-account')

    # Assert 200 success for now.
    # Testing to confirm orders made with account using /v1/orders would fall under Order Status APIs testing
    assert new_order.new_order_post().status_code == 200


@pytest.mark.positive
@pytest.mark.parametrize("value, expected_bool", [
    ("50", False),
    ("1000000", True)
])
def test_new_order_options_maker_or_cancel(value, expected_bool):
    """
        Verify New Order request when using options value "maker-or-cancel" and all orders can be filled then is_cancelled equals True
        Verify New Order request when using options value "maker-or-cancel" and no orders can be filled then is_cancelled equals False
    """
    new_order = NewOrder(symbol='btcusd',
                         amount='1',
                         price=value,
                         side='buy',
                         type='exchange limit',
                         options=["maker-or-cancel"])
    response = new_order.new_order_post()
    assert response.json().get('is_cancelled') is expected_bool


@pytest.mark.positive
@pytest.mark.parametrize("amount, expected_bool", [
    ("1", False),
    ("1000", True)
])
def test_new_order_options_immediate_or_cancel(amount, expected_bool):
    """
        Verify New Order request when using options value "immediate-or-cancel" all orders can be filled then is_cancelled equals True
        Verify New Order request when using options value "immediate-or-cancel" and all orders does fill immediately then is_cancelled equals False

    """
    new_order = NewOrder(symbol='btcusd',
                         amount=amount,
                         price='70000',
                         side='buy',
                         type='exchange limit',
                         options=["immediate-or-cancel"])
    response = new_order.new_order_post()
    assert response.json().get('is_cancelled') is expected_bool


@pytest.mark.positive
@pytest.mark.parametrize("amount, expected_bool", [
    # ("1", False),
    ("1000", True)
])
def test_new_order_options_fill_or_kill(amount, expected_bool):
    """
        Verify New Order request when using options value "fill-or-kill and all orders can be filled then is_cancelled equals False
        Verify New Order request when using options value "fill-or-kill and no orders can be filled then is_cancelled equals True

    """

    new_order = NewOrder(symbol='ethusd',
                         amount=amount,
                         price='4900',
                         side='buy',
                         type='exchange limit',
                         options=["fill-or-kill"])
    response = new_order.new_order_post()
    assert response.json().get('is_cancelled') is expected_bool


##################################
#                                #
#       Negative TCs:            #
#                                #
##################################

@pytest.mark.negative
@pytest.mark.parametrize("value, status_code", [
    ("invalid-api-key-test", 400),
    ("", 400)
    # Is this expected? API key is independent of signature in request header
])
def test_new_order_invalid_api_key(value, status_code):
    """
        Verify New Order request when using invalid api key then status code returns 400
        Verify New Order request when using empty api key then status code returns 400
    """
    new_order = NewOrder(symbol='ethusd',
                         amount='1',
                         price='5000',
                         side='buy',
                         type='exchange limit')

    new_order.api_key = value
    new_order.new_order_post()
    assert new_order.status_code == status_code

@pytest.mark.negative
@pytest.mark.parametrize("value, status_code", [
    ("invalid-gemini-signature-test", 400),
    ("", 400)
])
def test_new_order_invalid_api_secret(value, status_code):
    """
        Verify New Order request when using invalid api secret then status code returns 400
        Verify New Order request when using empty api secret then status code returns 400
    """
    new_order = NewOrder(symbol='ethusd',
                         amount='1',
                         price='5000',
                         side='buy',
                         type='exchange limit')
    new_header = new_order.headers
    new_header['X-GEMINI-SIGNATURE'] = value
    new_order.new_order_post(headers=new_header)
    assert new_order.status_code == status_code

@pytest.mark.negative
@pytest.mark.parametrize("value, status_code", [
    ("invalid-gemini-payload-test", 400),
    ("", 400)
])
def test_new_order_invalid_payload(value, status_code):
    """
        Verify New Order request when using invalid payload format then status code returns 400
        Verify New Order request when using empty payload format then status code returns 400
    """
    new_order = NewOrder(symbol='ethusd',
                         amount='1',
                         price='5000',
                         side='buy',
                         type='exchange limit')
    new_header = new_order.headers
    new_header['X-GEMINI-PAYLOAD'] = value
    new_order.new_order_post(headers=new_header)
    assert new_order.status_code == status_code

@pytest.mark.negative
@pytest.mark.parametrize("key, value, status_code, error_reason", [
    ("request", "/f1/gasly", 404, "EndpointNotFound"),
    ("nonce", 100.0, 400, "InvalidNonce"),
    ("client_order_id", 988764, 400, "ClientOrderIdMustBeString"),
    ("symbol", "NOTBTC", 400, "InvalidSymbol"),
    ("amount", "-100.0", 400, "InvalidQuantity"),
    # ("min_amount", "-1", 400, ""),  # Should this fail?
    ("price", "0", 400, "InvalidPrice"),
    ("side", "loan", 400, "InvalidSide"),
    ("type", "limit", 400, "InvalidOrderType"),
    ("options", "string-instead-of-list", 400, "OptionsMustBeArray"),
    # ("stop_price", "-100", 400, ""),  # Should this fail?
    # ("account", 100.201, 400, "")  # Should this fail?
])
def test_new_order_invalid_payload_values(key, value, status_code, error_reason):
    """
        Verify New Order request when using invalid payload then status code returns
        expected status code and error reason
    """
    new_order = NewOrder(symbol='ethusd',
                         amount='1',
                         price='5000',
                         side='buy',
                         type='exchange limit')
    new_order.__setattr__(key, value)
    new_order.new_order_post()
    assert new_order.status_code == status_code
    assert new_order.error_reason == error_reason

@pytest.mark.negative
@pytest.mark.parametrize("key, value, status_code, error_reason", [
    ("nonce", "", 400, "MissingNonce"),
    ("symbol", "", 400, "MissingSymbol"),
    ("amount", "", 400, "MissingQuantity"),
    ("price", "", 400, "MissingPrice"),
    ("side", "", 400, "MissingSide"),
    ("type", "", 400, "MissingOrderType")
])
def test_new_order_missing_payload_values(key, value, status_code, error_reason):
    """
        Verify New Order request when using missing payload key values then status code returns
    """
    new_order = NewOrder(symbol='ethusd',
                         amount='1',
                         price='5000',
                         side='buy',
                         type='exchange limit')
    new_order.__setattr__(key, value)
    new_order.new_order_post()
    assert new_order.status_code == status_code
    assert new_order.error_reason == error_reason




