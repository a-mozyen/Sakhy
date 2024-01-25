import requests


def get_token():
        url = "https://daleelapi.com/api/v1/oauth/token"

        payload = {
            'grant_type': 'password',
            'client_id': '2',
            'client_secret': 'D1uvg3aUd79fDIvqduYlaV3q1b59XztrPPooADyDrIo=',
            'username': 'merchants.api@daleelstore.com',
            'password': 'ABC12345'
            }
        
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.post(url=url, headers=headers, data=payload, verify=True)
        token = response.json()
        
        return print(token)

get_token()
