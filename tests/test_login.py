#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from test_base import *

class LoginTestCase(BaseTestCase):
    def test_login_page(self):
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 200)
        data = resp.text
        self.assertTrue(('Please use admin/admin to login at first time.' in data) or 
            ('Please input username and password.' in data))

    def test_login_wrong_parms(self):
        resp = self.client.post('/login', data={'username': '', 'password': 'password'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Username is empty.', resp.text)

        resp = self.client.post('/login', data={'username': '1111111111111111111111111111111111111111111111111', 'password': 'password'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('The len of username reached the limit of 25 chars.', resp.text)

        resp = self.client.post('/login', data={'username': '<kindleear>', 'password': 'password'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('The username includes unsafe chars.', resp.text)

        resp = self.client.post('/login', data={'username': 'admin', 'password': 'password'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('The username does not exist or password is wrong.', resp.text)

    def test_login_success(self):
        resp = self.client.post('/login', data={'username': 'admin', 'password': 'admin'})
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post('/logout')
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get('/logout')
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get('/needloginforajax')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {'status': 'login required'})
        
    def test_resetpwd(self):
        resp = self.client.get('/resetpwd')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Please input the correct username and email to reset password.', resp.text)

        resp = self.client.get('/resetpwd?name=admin')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Reset password', resp.text)
        
