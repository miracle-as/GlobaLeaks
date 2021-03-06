# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks

from globaleaks.tests import helpers
from globaleaks.handlers.admin import manifest


class TestManifestHandler(helpers.TestHandler):
    _handler = manifest.ManifestHandler

    @inlineCallbacks
    def test_get(self):
        handler = self.request({}, role='admin')

        response = yield handler.get()

        for k in ['changelog', 'version', 'license']:
            self.assertTrue(k in response)
