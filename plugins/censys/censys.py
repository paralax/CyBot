# !censys is used for Querying the censys.io API

import os, requests, json, re
from errbot import BotPlugin, botcmd, arg_botcmd

base_url = "https://www.censys.io/api/v1"
api_id = "changeme"
api_secret = "changeme"


class censys(BotPlugin):
    @arg_botcmd("query", type=str)  # flags a command
    def censys(self, msg, query=None):
        query = re.sub("[\[()\]]", "", query)
        uri = "view/ipv4/{}".format(query)
        response = requests.get(base_url + uri, auth=api_creds)
        json_resp = response.json()

        answer = "Status: " + json_resp["status"] + "\r\n"

        if json_resp.get("error", False):
            answer += json_resp["error"] + "\r\n"
        else:
            answer += "IP: {0}\r\n".format(", ".join(json_resp["ip"]))
            answer += "Tags: {0}\r\n".format(", ".join(json_resp["tags"]))
            answer += "Protocols: {0}\r\n".format(", ".join(json_resp["protocols"]))
            if (80) in json_resp["ports"]:
                try:
                    answer += "Web page title (80/http): {0}\r\n".format(
                        json_resp["80"]["http"]["get"]["title"]
                    )
                except KeyError:
                    pass
            if (443) in json_resp["ports"]:
                try:
                    answer += "Web page title (443/https): {0}\r\n".format(
                        json_resp["443"]["https"]["get"]["title"]
                    )
                except KeyError:
                    pass
            answer += "Updated at: {0}\r\n".format(", ".join(json_resp["updated_at"]))
        return answer
