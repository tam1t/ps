import requests
from settings import *
from platform import *
from base64 import b64encode
import json
import datetime
class Shipstation():
    def getOrderNumber(self, id, userAndPass):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + userAndPass.decode("ascii")
        }
        response = requests.get(SHIPSTATION_ENDPOINT['ORDERS'] + str(id) + "&storeId=" + SHIPSTATION_STOREIDS['SYSTUM'], headers=headers)
        if response.status_code == RESPONSE_STATUS['STATUS_OK']:
            return json.loads(response.content)
        return []

    def getAllShipments(self, userAndPass):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + userAndPass.decode("ascii")
        }
        response = requests.get(SHIPSTATION_ENDPOINT['SHIPMENTS'] + SHIPSTATION_STOREIDS['SYSTUM'], headers=headers)
        if response.status_code == RESPONSE_STATUS['STATUS_OK']:
            return json.loads(response.content)
        return []

    def getShipmentByOrderNumber(self, sysid, userAndPass):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + userAndPass.decode("ascii")
        }
        response = requests.get(SHIPSTATION_ENDPOINT['FULFILLMENT_ORDERNUM_PARAM'] + str(sysid) + "&storeId="+SHIPSTATION_STOREIDS['SYSTUM'], headers=headers)
        if response.status_code == RESPONSE_STATUS['STATUS_OK']:
            return json.loads(response.content)
        return []


    def prepareItems(self, salesOrderItems):
        shipStationItems = []
        for orderItem in salesOrderItems:
            itemJson = {}
            weightJson = {}
            customFieldShipStationId = None
            itemJson['lineItemKey']  = ""
            if orderItem['sku'] is not None:
                itemJson['sku'] = orderItem['sku']
            for customField in orderItem['customFields']:
                for customId in customField:
                        if customId == "ShipStationID" is not None:
                            customFieldShipStationId = customField['ShipStationID']
            if customFieldShipStationId is not None:
                itemJson['sku']          = customFieldShipStationId
            if orderItem['name'] == "NONAME":
                itemJson['name']         = orderItem['product']['name']
            else:
                itemJson['name'] = orderItem['name']

            weightJson['value']      = orderItem['unitWeight']
            weightJson['units']      = orderItem['weightMeasure']

            itemJson['weight']       = weightJson

            itemJson['quantity']     = orderItem['quantity']
            itemJson['unitPrice']    = orderItem['price']
            itemJson['warehouseLocation'] = ""
            itemJson['productId'] = orderItem['sysid']
            itemJson['upc'] = ""

            shipStationItems.append(itemJson)

        return shipStationItems

    def createOrder(self, orderSysId, formNumber, auth_token, userAndPass):
        systum_platform = Platform()

        now = datetime.datetime.now()

        sales_order_detail = systum_platform.get_sales_order_by_id(auth_token, orderSysId)
        salesOrderSysId = sales_order_detail['sysid']
        customerName = sales_order_detail['customer']['name']
        customerShipToName = sales_order_detail['shippingAddress']['name']
        customerShipAddress1 = sales_order_detail['shippingAddress']['street1']
        street2 = sales_order_detail['shippingAddress'].get('street2', None)
        customerShipAddress2 = ""
        if street2 is not None:
            customerShipAddress2 = street2
        customerShipAddressCity = sales_order_detail['shippingAddress']['city']
        customerShipAddressState = sales_order_detail['shippingAddress']['locale']
        customerShipAddressCountry = sales_order_detail['shippingAddress']['country']
        customerShipAddressZip = sales_order_detail['shippingAddress']['postCode']
        #customerPhone = sales_order_detail['customer']['phone']
        customerPhone = ""
        customerName = sales_order_detail['customer']['name']
        customerEmail = sales_order_detail['customer']['email']
        salesOrderItems = sales_order_detail['items']
        orderItems = self.prepareItems(salesOrderItems)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + userAndPass.decode("ascii")
        }
        params = {
            "orderNumber": formNumber,
            "orderDate": str(now),
            "orderStatus": SHIPSTATION_ENDPOINT['AWAITING_SHIPMENT'],
            "customerUsername": customerName,
            "customerEmail": customerEmail,
            "taxAmount": sales_order_detail['tax'],
            "billTo": {
                "name": customerName,
            },
            "shipTo": {
                "name": customerName,
                "company": customerName,
                "street1": customerShipAddress1,
                "street2": customerShipAddress2,
                "city": customerShipAddressCity,
                "state": us_state_abbrev[0][customerShipAddressState],
                "postalCode": customerShipAddressZip,
                "country": countries_abbrev[0][customerShipAddressCountry],
                "phone": customerPhone
            },
            "items": json.loads(json.dumps(orderItems, indent=4)),
            "advancedOptions": {
                "storeId": SHIPSTATION_STOREIDS['SYSTUM']
            }
        }
        if orderItems:
            response = requests.post(SHIPSTATION_ENDPOINT['CREATE_ORDER'], headers=headers, json=json.loads(json.dumps(params, indent=4)))
            print(response)

    def processOrder(self, auth_token, userAndPass):
        systumPlatform = Platform()
        shipmentsTracking = []
        shipments = self.getAllShipments(userAndPass)
        fulfillBy3PLOrders = systumPlatform.get3PLSalesOrders(auth_token)
        for order in fulfillBy3PLOrders:
            if not self.getOrderNumber(order['formNumber'], userAndPass)['orders']:
                self.createOrder(order['sysid'], order['formNumber'], auth_token, userAndPass)
            orderShipment = self.getShipmentByOrderNumber(order['formNumber'], userAndPass)
            orderInSystum = systumPlatform.get_sales_order_by_id(auth_token, order['sysid'])
            if orderInSystum:
                if orderShipment['fulfillments']:
                    for ssFulfillment in orderShipment['fulfillments']:
                        if ssFulfillment['orderNumber'] == str(orderInSystum['formNumber']):
                            trackingNumber = ssFulfillment['trackingNumber']
                            shippingCost = ssFulfillment['fulfillmentFee']

                            fulfillmentPackage = systumPlatform.getFulfillmentShipmentPackage(auth_token,
                                                                                              orderInSystum['sysid'])
                            packageId = fulfillmentPackage[0]['shippedPackage'][0]['sysid']

                            systumPlatform.saveTrackingNumber(auth_token, orderInSystum['sysid'], packageId, trackingNumber,
                                                              shippingCost)
                            systumPlatform.fulfillSalesOrder(auth_token, orderInSystum['sysid'], 'FULFILLED')

