SHIPSTATION_ENDPOINT = dict(
    ORDERS = "https://ssapi.shipstation.com/orders/?orderNumber=",
    CREATE_ORDER = "https://ssapi.shipstation.com/orders/createorder",
    SHIPMENTS = "https://ssapi.shipstation.com/shipments?storeId=",
    FULFILLMENT_ORDERNUM_PARAM = "https://ssapi.shipstation.com/fulfillments?orderNumber",
    SHIPMENTS_ORDERNUM_PARAM = "https://ssapi.shipstation.com/shipments?orderNumber=",
    AWAITING_SHIPMENT = "awaiting_shipment"
)
SYSTUM_ENDPOINT = dict(
    EMPLOYEE_AUTH = "https://receptra.systum.com/api/identity/auth/employee/",
    GET_SALES_ORDER = "https://receptra.systum.com/api/sales-orders/",
    PURCHASE_ORDER = "/api/purchase-orders/"
)
RESPONSE_STATUS = dict(
    STATUS_OK = 200
)
SHIPSTATION_STOREIDS = {
    'SYSTUM': "376181"
}
countries_abbrev = {
    'United States': 'US'
},
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}