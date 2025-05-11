import requests, base64, time

class TidalClient:
    TOKEN_URL = 'https://auth.tidal.com/v1/oauth2/token'
    API_BASE  = 'https://api.tidal.com/v1'

    def __init__(self, client_id: str, client_secret: str, country_code='US'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.country_code = country_code
        self._token = None
        self._expires_at = 0

    def _authenticate(self):
        auth_str = f"{self.client_id}:{self.client_secret}"
        b64 = base64.b64encode(auth_str.encode()).decode()
        headers = {
            'Authorization': f'Basic {b64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {'grant_type': 'client_credentials'}
        resp = requests.post(self.TOKEN_URL, headers=headers, data=data)
        resp.raise_for_status()
        j = resp.json()
        self._token = j['access_token']
        self._expires_at = time.time() + j.get('expires_in', 3600) - 60

    def _ensure_token(self):
        if not self._token or time.time() >= self._expires_at:
            self._authenticate()

    def _request(self, method: str, path: str, **kwargs):
        self._ensure_token()
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f"Bearer {self._token}"
        params = kwargs.pop('params', {}) or {}
        if 'countryCode' not in params:
            params['countryCode'] = self.country_code
        url = f"{self.API_BASE}{path}"
        return requests.request(method, url, headers=headers, params=params, **kwargs)

    def search_tracks(self, q: str, limit=20, offset=0):
        params = {
            'query': q,
            'types': 'TRACKS',
            'limit': limit,
            'offset': offset
        }
        r = self._request('GET', '/search', params=params)
        r.raise_for_status()
        data = r.json().get('data', [])
        return [
            {
                'id':    item['id'],
                'title': item['attributes']['name'],
                'artist': item['attributes']['artistName']
            } for item in data
        ]
