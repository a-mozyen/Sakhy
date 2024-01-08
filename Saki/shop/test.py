import requests


def get_token():
        response = requests.post(
                url="https://daleelapi.com/api/v1/oauth/token", 
                headers={
                    'Content-Type': 'application/json'
                    }, 
                data={
                    'grant_type':'password',
                    'client_id':'2',
                    'client_secret':'D1uvg3aUd79fDIvqduYlaV3q1b59XztrPPooADyDrIo=',
                    'username':'merchants.api@daleelstore.com',
                    'password':'ABC12345'
                    }
                )
        
        token = response.json()
        return print(token)

get_token()
