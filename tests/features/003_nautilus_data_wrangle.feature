Feature: CondorGp's evolutions need fitness checking against data
  As a gp algorithm reliant on data,
  Data must be found, wrangled and correctly available
  To allow backtesting.

# wrangle data into bars
  Scenario Outline: When a csv of binance data is ready
    Given no bar Nautilus objects
    When a data wrangle is run
    Then an object of type XXX is added

# wrangled data is correctly formatted
  Scenario Outline: Binance wrangled data format works
    Given a bar Nautilus object
    When formatting is checked
    Then the bar formatting fits
