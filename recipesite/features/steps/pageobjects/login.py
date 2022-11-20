from recipesite.features.browser import Browser

class LoginPage(Browser):

    LOGIN = '/login'
    LOGOUT = '/logout'

    def log_in(self, username, password):
        """
        Locate and input values to the user and password fields and submit the form
        :param username:
        :param password:
        """
        username_field = self.query_selector_css('.form-control[name="username"]')
        username_field.send_keys(username)
        password_field = self.query_selector_css('.form-control[name="password"]')
        password_field.send_keys(password)
        login_button = self.query_selector_css('.btn-success')
        login_button.click()

    def log_out(self):
        """
        Visit the logout page
        """
        self.visit(LoginPage.LOGOUT)