# /features/scrape.feature
Feature: Login
    As a user
    I should be able to login and verify results.

    Scenario: Login User
        Given I log into the site login
        Then I should visit homepage
