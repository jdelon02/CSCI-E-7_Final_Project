# /features/scrape.feature
Feature: Scrape Recipe
  As a user
  I should be able to scrape a recipe from a website and verify results.

  Scenario: Load Scrape Page
    Given I log into the site
    Given I visit the scrape page
    # use your own steps using selenium-requests features
    Then I expect the response to be parsed as recipe
    Then I expect the ingrdeients to not be empty