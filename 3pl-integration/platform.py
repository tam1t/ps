import urllib.request
import requests
from settings import *
import json
class Platform():

    def get_auth_token(self, grant_type, domain, username, password):
        params = {
            "grant_type": grant_type,
            "domain": domain,
            "username": username,
            "password": password
        }
        req = urllib.request.Request(SYSTUM_ENDPOINT['EMPLOYEE_AUTH'], method='POST')
        data = urllib.parse.urlencode(params).encode('utf-8')
        with urllib.request.urlopen(req, data) as response:
            json_obj = json.loads(response.read().decode('utf-8'))
            return json_obj['token']

    def fulfill_sales_order_by_id(self, auth_token, id, shipping_tracking_number):
        sales_order_json = self.get_sales_order_by_id(auth_token, id)
        items = sales_order_json['items']
        for so_items in items:
            so_item_id = so_items['sysid']
            so_price = so_items['price']
            so_quantity = so_items['quantity']

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token " + auth_token
        }
        params = {
            "fulfillments": [{
                "quantityFulfilled": so_quantity,
                "itemId": so_item_id,
                "shippingTrackingNo": shipping_tracking_number
            }]
        }
        # Fulfill sales order
        req = urllib.request.Request(SYSTUM_ENDPOINT['GET_SALES_ORDER'] + id + "/fulfillment/", method='POST', headers=headers)
        data = json.dumps(params).encode("utf-8")
        with urllib.request.urlopen(req, data) as response:
            print(response.read().decode('utf-8'))
            print("done fulfilling")


    def get_sales_order_by_id(self, auth_token, id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token "+auth_token
        }
        response = requests.get(SYSTUM_ENDPOINT['GET_SALES_ORDER'] + str(id) + "/", headers=headers)
        if response.status_code == RESPONSE_STATUS['STATUS_OK']:
            return json.loads(response.content)
        return []


    def updateSalesOrderTitle(self, auth_token, id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token " + auth_token
        }
        params = {
            "title":  TEST_VARIABLES["SALES_ORDER_SMARTFILL_TITLE"]
        }
        req = urllib.request.Request(SYSTUM_ENDPOINT['GET_SALES_ORDER'] + id + "/", method='POST', headers=headers)
        data = json.dumps(params).encode("utf-8")
        with urllib.request.urlopen(req, data) as response:
            print(response.read().decode('utf-8'))
            print("done fulfilling sales order, updating title")

    def saveTrackingNumber(self, auth_token, sysid, packageId, trackingNumber, shippingCost):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token " + auth_token
        }
        params = {
            'shippingTrackingNo': trackingNumber,
            'shippingLabelId': trackingNumber,
            'actualShippingCost': shippingCost
        }
        requests.post(SYSTUM_ENDPOINT['GET_SALES_ORDER'] + str(sysid) + '/packages/' + str(packageId) + '/', data=json.dumps(params), headers=headers)

    def fulfillSalesOrder(self, auth_token, sysid, status):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token " + auth_token
        }
        params = {
            'status': status
        }
        requests.post(SYSTUM_ENDPOINT['GET_SALES_ORDER']+str(sysid)+'/', data=json.dumps(params), headers=headers)


    def getFulfillmentShipmentPackage(self, auth_token, sysid):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token " + auth_token
        }
        response = requests.get(SYSTUM_ENDPOINT['GET_SALES_ORDER'] + str(sysid) + "/fulfillment/", headers=headers)
        if response.status_code == RESPONSE_STATUS['STATUS_OK']:
            return json.loads(response.content)
        return []


    def get3PLSalesOrders(self, auth_token):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token " + auth_token
        }
        response = requests.get(SYSTUM_ENDPOINT[
                               'GET_SALES_ORDER'] + '?is3PLFulfillment=true&status=PENDING_FULFILLMENT,PARTIALLY_FULFILLED,APPROVED', headers=headers)
        return json.loads(response.content)



