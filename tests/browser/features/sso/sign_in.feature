@sso
Feature: Sign in

  Background:
    Given basic authentication is done for "Single Sign-On - Sign in" page

  Scenario:
    Given "Robert" visits the "Single Sign-On - Sign in" page

    When "Robert" decides to "register"

    Then "Robert" should be on the "Single Sign-On - Registration" page
