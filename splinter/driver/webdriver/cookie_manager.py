# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from urlparse import urlparse
from splinter.cookie_manager import CookieManagerAPI


class CookieManager(CookieManagerAPI):

    def __init__(self, driver):
        self.driver = driver

    def add(self, cookies):
        for key, value in cookies.items():
            self.driver.add_cookie({'name': key, 'value': value})

    def delete(self, *cookies):
        if cookies:
            for cookie in cookies:
                self.driver.delete_cookie(cookie)
        else:
            self.driver.delete_all_cookies()

    def all(self, info=False):
        if not info:
            cleaned_cookies = []
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                cookie_domain = cookie['domain'] if not cookie['domain'].startswith('.') else cookie['domain'][1:]
                if cookie_domain in urlparse(self.driver.current_url).netloc:
                    cookie = {cookie['name']: cookie['value']}
                    cleaned_cookies.append(cookie)
            return cleaned_cookies
        return self.driver.get_cookies()

    def __getitem__(self, item):
        return self.driver.get_cookie(item)['value']

    def __eq__(self, other_object):
        cookies = {}
        for cookie in self.driver.get_cookies():
            cookies[cookie['name']] = cookie['value']

        if isinstance(other_object, dict):
            return dict(cookies) == other_object
