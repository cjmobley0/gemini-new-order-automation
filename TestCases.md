Order Placement APIs - New Order Test Cases

Positive Happy Path TCs:
Verify New Order POST request returns 200 status
Verify New Order POST request returns a JSON when using the following fields and types:
    order_id: string
    id: string
    symbol: string
    exchange: string
    avg_execution_price: string
    side: string
    type: string
    timestamp: string
    timestampms: integer
    is_live: boolean
    is_cancelled: boolean
    is_hidden: boolean
    was_forced: boolean
    executed_amount: string
    options: array
    price: string
    original_amount: string
    remaining_amount; string
    
Verify New Order POST request nonce value matches the JSON response timestamp value
Verify New Order POST request amount value matches the JSON response original_amount value
    1
    0.4
    
Verify New Order POST request price value matches the JSON response price value
    100
    10.0
    
Verify New Order POST request side value matches the JSON response side value
    buy
    sell
    
Verify New Order POST request type value matches the JSON response type value
    exchange limit: exchange limit
    exchange stop limit: stop-limit

Positive Optional Parameters TCs:
Verify New Order POST request client_order_id value matches the JSON response client_order_id value
Verify New Order POST request stop_price value for buy and sell returns 200 response
Verify New Order POST request account value return 200 response
Verify New Order request when using options value "maker-or-cancel" and all orders can be filled then is_cancelled equals True
Verify New Order request when using options value "maker-or-cancel" and no orders can be filled then is_cancelled equals False
Verify New Order request when using options value "immediate-or-cancel" and all orders doesn't fill immediately then is_cancelled equals True
Verify New Order request when using options value "immediate-or-cancel" and all orders does fill immediately then is_cancelled equals False
Verify New Order request when using options value "fill-or-kill and all orders can be filled then is_cancelled equals False
Verify New Order request when using options value "fill-or-kill and no orders can be filled then is_cancelled equals True
Verify New Order request when using options value "auction-only" then the order will be added to the auction-only book
Verify New Order request when using options value "indication-of-interest" then the order will remain active for 60 seconds


Negative TCs:
Verify New Order request when using invalid api key then status code returns 400
Verify New Order request when using empty api key then status code returns 400
Verify New Order request when using invalid api secret then status code returns 400
Verify New Order request when using empty api secret then status code returns 400
Verify New Order request when using invalid payload format then status code returns 400
Verify New Order request when using empty payload format then status code returns 400

Verify New Order request when using invalid payload then status code returns expected status code and error reason
    "request", "/f1/gasly", 404, "EndpointNotFound" 
    "nonce", 100.0, 400, "InvalidNonce"
    "client_order_id", 988764, 400, "ClientOrderIdMustBeString"
    "symbol", "NOTBTC", 400, "InvalidSymbol"
    "amount", "-100.0", 400, "InvalidQuantity"
    "price", "0", 400, "InvalidPrice"
    "side", "loan", 400, "InvalidSide"
    "type", "limit", 400, "InvalidOrderType"
    "options", "string-instead-of-list", 400, "OptionsMustBeArray"
    
Verify New Order request when using missing payload key values then status code returns 400
    "nonce", "", 400, "MissingNonce"
    "symbol", "", 400, "MissingSymbol"
    "amount", "", 400, "MissingQuantity"
    "price", "", 400, "MissingPrice"
    "side", "", 400, "MissingSide"
    "type", "", 400, "MissingOrderType"
    

Possible Bugs:
Using invalid or empty X-GEMINI-APIKEY and valid X-GEMINI-SIGNATURE returns InvalidSignature
Using integer values for New Order optional parameters min_amount, stop_price, account returns status code 200
Using float values for New Order optional parameters min_amount, stop_price, account returns status code 200
Using negative values for New Order optional parameters min_amount, stop_price, account returns status code 200 

