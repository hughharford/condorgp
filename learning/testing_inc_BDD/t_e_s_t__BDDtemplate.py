from pytest_bdd import scenarios, given, when, then

# Scenario: Add two integers
# Given integers a and b
# When a and b are added
# Then the result is a+b

# NOT: scenario('../../features/C_S/c001_add.feature', 'Add two integers')
# USE:
scenarios('../features/C_S/c001_add.feature')


# def test_add():
#     """
#     NOTE: Relative paths here are critical,
#     depth of folder to be reflected in ../../ etc
#
#     THIS TEST_ADD SHOULD NOT BE REQUIRED>>>
#
#     """
#     pass


@given('integers a and b')
def given_integers():
    pass


@when('a and b are added')
def when_added():
    pass


@then('the result is a+b')
def then_result():
    assert 1001 == 1002
