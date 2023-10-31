import jwt
import time


def generate_jwt(private_key_json):
    iat = time.time()
    exp = iat + 3600

    service_email = private_key_json['client_email']
    private_key_id = private_key_json['private_key_id']
    private_key = private_key_json['private_key']

    payload = {'iss': service_email,
               'sub': service_email,
               'aud': 'https://accounts.google.com/o/oauth2/token',
               'iat': iat,
               'exp': exp,
               'scope': 'https://www.googleapis.com/auth/drive'}
    
    additional_headers = {'kid': private_key_id}

    signed_jwt = jwt.encode(payload, private_key, headers=additional_headers, algorithm='RS256')

    return signed_jwt


def get_request_body(boundary, file_content, metadata):
    body = f"""
--{boundary}
Content-Type: application/json; charset=UTF-8

{f'{metadata}'}

--{boundary}
Content-Type: text/plain

{file_content}

--{boundary}--
"""
    return body