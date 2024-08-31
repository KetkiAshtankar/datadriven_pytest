import pytest
import csv
import os
from pages.login_page import LoginPage

def get_login_data():
    login_data = []
    # Get the directory of the current script
    current_dir = os.path.dirname(__file__)
    # Construct the correct path to the CSV file
    data_file = os.path.join(current_dir, '../data', 'login_data.csv')

    # Read the CSV file
    with open(data_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Ensure each row is treated as a dictionary
            username = row['username']
            password = row['password']
            login_data.append((username, password))
    return login_data

@pytest.mark.usefixtures("setup")
class TestLogin:

    @pytest.mark.parametrize("username, password", get_login_data())
    def test_login(self, username, password):
        login_page = LoginPage(self.driver)
        login_page.login(username, password)
        assert "inventory.html" in self.driver.current_url
