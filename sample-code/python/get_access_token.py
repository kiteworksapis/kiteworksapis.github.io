#!/usr/bin/env python
# File: python/get_access_token.py

import time
import requests
import webview
from urllib.parse import urlparse, parse_qs
import base64
import hashlib
import os

class KWOAuthClient:
    def __init__(self, base_url):
        self.authorization_endpoint = f"{base_url}/oauth/authorize"
        self.token_endpoint = f"{base_url}/oauth/token"
        self.redirect_uri = f"{base_url}/rest/callback.html"
        self._credential_manager = _CredentialManager()

    @staticmethod
    def _generate_pkce_pair():
        code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).rstrip(b'=').decode('utf-8')
        return code_verifier, code_challenge

    def _is_token_expired(self):
        token_data = self._credential_manager.retrieve_saved_access_token()
        if token_data is None:
            return True
        # Check if current time >= expiry
        return int(time.time()) >= token_data['expiry']

    def _refresh_access_token(self):
        refresh_token = self._credential_manager.retrieve_saved_refresh_token()
        if not refresh_token:
            raise ValueError("No refresh token available.")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self._credential_manager.get_client_id(),
            "client_secret": self._credential_manager.get_client_secret()
        }

        response = requests.post(self.token_endpoint, data=data)
        response.raise_for_status()
        return response.json()

    def _exchange_code_for_tokens(self, code, code_verifier):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self._credential_manager.get_client_id(),
            "client_secret": self._credential_manager.get_client_secret(),
            "code_verifier": code_verifier
        }

        response = requests.post(self.token_endpoint, data=data)
        response.raise_for_status()
        return response.json()

    def _save_tokens(self, tokens):
        expires_at = int(time.time()) + tokens.get('expires_in', 3600)
        self._credential_manager.save_tokens(tokens['access_token'], tokens.get('refresh_token'), expires_at)

    def _poll_url(self, window, timeout=60):
        start = time.time()
        while True:
            current_url = window.get_current_url()
            if current_url.startswith(self.redirect_uri):
                parsed = urlparse(current_url)
                qs = parse_qs(parsed.query)
                if "code" in qs:
                    self.auth_code = qs["code"][0]
                    window.destroy()
                    break
            if (time.time() - start) > timeout:
                print("Timeout waiting for redirect.")
                window.destroy()
                break
            time.sleep(0.5)

    def _start_oauth_flow(self, code_challenge):
        auth_url = (
            f"{self.authorization_endpoint}?client_id={self._credential_manager.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&response_type=code"
            f"&code_challenge={code_challenge}"
            f"&code_challenge_method=S256"
        )

        window = webview.create_window("Login", auth_url)
        # poll the window until the redirect or a timeout
        webview.start(lambda: self._poll_url(window))
        return self.auth_code

    def get_access_token(self):
        # 1) Retrieve access token if token is not expired
        if not self._is_token_expired():
            saved_token = self._credential_manager.retrieve_saved_access_token()
            return saved_token['access_token']

        # 2) If we have a refresh token, try to refresh
        if self._credential_manager.retrieve_saved_refresh_token() is not None:
            try:
                print("Refreshing access token...")
                tokens = self._refresh_access_token()
                self._save_tokens(tokens)
                return tokens["access_token"]
            except Exception as e:
                print("Failed to refresh token:", e)

        # 3) Otherwise, start the OAuth flow
        code_verifier, code_challenge = self._generate_pkce_pair()
        print("Reauthentication required. Opening browser to obtain new token...")
        code = self._start_oauth_flow(code_challenge)
        if not code:
            raise RuntimeError("No authorization code obtained (timeout?).")

        tokens = self._exchange_code_for_tokens(code, code_verifier)
        self._save_tokens(tokens)
        return tokens["access_token"]

class _CredentialManager:
    """
    A simple in-memory credential manager for demonstration purposes.
    # In production, use a secure store.
    """
    def __init__(self):
        self.token_data = None  # format: {'access_token':..., 'refresh_token':..., 'expiry':...}
        self.client_id = input("Enter your Client ID: ")
        self.client_secret = input("Enter your Client Secret: ")

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret

    def save_tokens(self, access_token, refresh_token, expiry):
        self.token_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expiry': expiry
        }

    def retrieve_saved_access_token(self):
        return self.token_data

    def retrieve_saved_refresh_token(self):
        if self.token_data and 'refresh_token' in self.token_data:
            return self.token_data['refresh_token']
        return None


if __name__ == "__main__":
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    token = client.get_access_token()
    print("Got access token:", token)