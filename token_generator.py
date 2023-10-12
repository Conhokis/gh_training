#!/usr/bin/env python3
import jwt
import time
import sys

def generate_token():
    pem = "god-is-watching-your-commits.2023-10-12.private-key.pem"
    app_id = "407147"

    # Open PEM
    with open(pem, 'rb') as pem_file:
        signing_key = jwt.jwk_from_pem(pem_file.read())

    payload = {
        # Issued at time
        'iat': int(time.time()),
        # JWT expiration time (10 minutes maximum)
        'exp': int(time.time()) + 600,
        # GitHub App's identifier
        'iss': app_id
    }

    # Create JWT
    jwt_instance = jwt.JWT()
    return jwt_instance.encode(payload, signing_key, alg='RS256')

