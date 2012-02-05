import urllib2


class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

class Checker(object):

    def __init__(self,timeout=2, agent="brodul/1.0"):
        self.timeout = timeout
        self.agent = agent
        self.opener = urllib2.build_opener()

    def build_request(self):
        if not self.url.startswith("http"):
            tmp = "http://" + self.url
            self.hurl = tmp
        request = urllib2.Request(self.hurl)
        request.add_header('User-Agent', self.agent)
        request.add_header('Accept-encoding', 'gzip')
        return request

    def get_code(self):
        try:
            response = self.opener.open(self.build_request())
            if hasattr(response, 'status'):
                return (self.url, response.status)
            else:
                return (self.url, response.code)
        except urllib2.HTTPError, e:
            return (self.url, e.code)
        except urllib2.URLError, e:
            return (self.url, e.reason)

    def check_url(self):
        code = self.get_code()
        ok, foo = None, None
        if code[1] in (200, 301, 302):
            ok = code
        else:
            foo = code

        return (ok, foo)
