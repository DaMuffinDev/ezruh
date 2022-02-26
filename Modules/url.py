from Resources.required_modules import pymodules
pymodules.install(pymodules.presets.modules("url"))

from Resources._variables import getitem_init, getitem_call
import requests

class __bitly:
    __init__ = getitem_init
    __call__ = getitem_call

    api_link = "https://api-ssl.bitly.com"

    def token(self, username, password):
        res = requests.post(self.api_link + "/oauth/access_token", auth=(username, password))
        return res.content.decode() if res.status_code == 200 else res.status_code 
    
    def guid(self, access_token):
        res = requests.get(self.api_link + "/v4/groups", headers={"Authorization": f"Bearer {access_token}"})
        return res.json()["groups"][0]["guid"] if res.status_code == 200 else res.status_code

    def link(self, link, guid, access_token):
        res = requests.post(self.api_link + "/v4/shorten", json={"group_guid": guid, "long_url": link}, headers={"Authorization": f"Bearer {access_token}"})
        return res.json().get("link") if res.status_code == 200 else res.status_code

@__bitly
def bitly(self, link, username, password):
    token = self.token(username, password)
    guid = self.guid(token)
    return self.link(link=link, guid=guid, access_token=token)