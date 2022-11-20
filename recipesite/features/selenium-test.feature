# /features/selenium-test.feature
Feature: Using selenium remote
  As a developer
  I should be able to connect to selenium grid on remote machines that are registered.

  Scenario: Load homepage
    # use a behave-webdriver step
    # use your own steps using selenium-requests features
    Given I send a GET request to the page "recipe"
    Then I expect the response text contains "Recipe Keeper"