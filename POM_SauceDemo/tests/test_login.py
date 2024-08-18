import pytest
import csv
from pages.login_page import LoginPage


def get_login_data():
    login_data = []
    with open('data/login_data.csv', newline='') as file:
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

