# {{ ansible_managed }}

import sys, os
import httplib
import ssl
from checks import AgentCheck

class SymfonyCheck(AgentCheck):
    def check(self, instance):
        if 'lock_files' not in instance:
            self.log.info("Skipping instance, no path to composer.lock found.")
            return

        lock_files = instance.get('lock_files', [])

        vulnerability_count = 0

        for file in lock_files:
            vulnerability_count += int(self.post_multipart('security.symfony.com', '/check_lock', file))

        self.gauge('symfony.core.vulnerabilities', vulnerability_count)

    def post_multipart(self, host, uri, file):
        ssl._create_default_https_context = ssl._create_unverified_context

        file = {
            'name':'lock',
            'filename': 'composer.lock',
            'content': open(file).read()
        }

        content_type, body = self.encode_multipart_formdata(file)

        conn = httplib.HTTPSConnection(host)
        conn.putrequest('POST', uri)
        conn.putheader('Accept', 'application/json')
        conn.putheader('Content-Length', str(len(body)))
        conn.putheader('Content-Type', content_type)
        conn.endheaders()
        conn.send(body)

        return conn.getresponse().getheader('X-Alerts')

    def encode_multipart_formdata(self, file):
        BOUNDARY = '----------------------------------_$'
        CRLF = '\r\n'

        L = []
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (file['name'], file['filename']))
        L.append('Content-Type: %s' % 'application/octet-stream')
        L.append('')
        L.append(file['content'])
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body
