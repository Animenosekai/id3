from time import time
from requests import Session as BaseSession
from id3.cache import LRUDictCache


class Session(BaseSession):
    """
    A normal requests.Session object which has GET requests cached for a specified duration.
    """

    def __init__(self, cache_duration: float = 3600) -> None:
        super().__init__()
        self.cache_duration = float(cache_duration)
        self.cache = LRUDictCache()

    def request(self, method: str, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None, allow_redirects=None, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
        method = method.upper()
        cache_key = f"{url}{params}{headers}{cookies}{files}{auth}"
        try:
            if method == "GET" and cache_key in self.cache:
                cache_item = self.cache[cache_key]
                if time() - cache_item["time"] <= self.cache_duration:
                    return cache_item["response"]
                self.cache.pop(cache_key, None)
        except Exception:
            pass
        r = super().request(method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects, proxies, hooks, stream, verify, cert, json)
        if method == "GET":
            self.cache[cache_key] = {"response": r, "time": time()}
        return r
