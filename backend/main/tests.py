from django.test import TestCase
import os
import pandas as pd
from .views import parse_spreadsheet
from .models import User, Team, Family
# Create your tests here.
class CsvTest(TestCase):
    def test_index(self):
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Good'})
    
    def test_parse_spreadsheet(self):
        df = pd.read_excel(os.path.join(os.path.dirname(__file__), 'test.xlsx'), engine="openpyxl")
        
        (
            new,
            existing,
            errors,
            new_users,
            existing_users,
            error_rows,
        ) = parse_spreadsheet(df)

        self.assertEqual(new, 7)
        self.assertEqual(existing, 0)
        self.assertEqual(errors, 3)

        users = User.objects.all()
        self.assertEqual(len(users), 7)
        teams = Team.objects.all()
        self.assertEqual(len(teams), 6)
        families = Family.objects.all()
        self.assertEqual(len(families), 1)

        (
            new,
            existing,
            errors,
            new_users,
            existing_users,
            error_rows,
        ) = parse_spreadsheet(df)

        self.assertEqual(new, 0)
        self.assertEqual(existing, 7)
        self.assertEqual(errors, 3)

        users = User.objects.all()
        self.assertEqual(len(users), 7)
        teams = Team.objects.all()
        self.assertEqual(len(teams), 6)
        families = Family.objects.all()
        self.assertEqual(len(families), 1)


