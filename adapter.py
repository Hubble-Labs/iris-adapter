from bridge import Bridge

import base64
from PIL import Image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

class Adapter:
    base_url = 'https://min-api.cryptocompare.com/data/price'
    from_params = ['base', 'from', 'coin']
    to_params = ['quote', 'to', 'market']

    def __init__(self, input):
        self.id = input.get('id', '1')
        #input data to external adapter to customize api request
        self.request_data = input.get('data')
        if self.validate_request_data():
            #bridge
            self.bridge = Bridge()
            self.set_params()
            self.create_request()
        else:
            #send error if request data is not valid
            self.result_error('No data provided')

    #makes sure request data is in correct format
    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    #take input request data and structure parameters used in api request
    def set_params(self):
        for param in self.from_params:
            self.from_param = self.request_data.get(param)
            if self.from_param is not None:
                break
        for param in self.to_params:
            self.to_param = self.request_data.get(param)
            if self.to_param is not None:
                break

    #takes data with parameters set and turns it into a request for the api
    def create_request(self):
        try:
            params = {
                'fsym': self.from_param,
                'tsyms': self.to_param,
            }
            #get response and parse it
            response = self.bridge.request(self.base_url, params)
            data = response.json()
            self.result = data[self.to_param]
            data['result'] = self.result

            # --- TEST --- #

            image_path = "test1.jpg"
            encoded_string = encode_image(image_path)
            self.result_success(encoded_string)

            # --- END TEST --- #

        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, data):
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'result': self.result,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
