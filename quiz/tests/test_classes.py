import unittest
from unittest import TestCase

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from ..quiz  import app,db, User, Score



class ModelTestCase(TestCase):
    def create_app(self):
        app = self.create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app


if __name__ == '__main__':
    with app.app_context():
        unittest.main()
