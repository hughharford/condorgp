# A key requirement is to provide strongly typed GP in Python
  This will allow specification for parameter inputs to functions etc


  ## Sample challenge: Enable calling get_config_strategy as shown below.
  cf: condorgp/evaluation/nautilus/cgp_naut_strategies.py

      def get_config_strategy(self):
        config = EMACrossConfig(
            instrument_id=str(self.instrument.id),
            bar_type=self.bar_type,
            trade_size=Decimal(1_000_000),
            fast_ema_period=100,
            slow_ema_period=200,
            )
        return config

  ## Explicit python declaration expects as above is difficult (trifficult):
  A parmeter for the function, bar_type is passed as:
    bar_type=input_variable_for_bar_type

  ## Making it less explicit solves the issue immediately.
  Less explicitness could be countered by provided an explict name, so that
    for looking through the code, the "name output" is explicit and readable

  # TRYING: Successful
  Calling the function without the explicit parameters.
    That works, so this is at least functional.

  # TRYING:
  A first basic pset to call get_config_strategy_without_full_declaration.
  It will need to be able to replicate this:

      def get_config_strategy_without_full_declaration(self):
        config = EMACrossConfig(
            str(self.instrument.id),
            self.bar_type,
            Decimal(1_000_000),
            100,
            200,
            )
        return config

  Types will be needed for:
    function_defintion - park this for later - get the first types up first
    string - for: instrument_id
    string - for: bar_type
    Decimal - for: trade_size
    int - for: fast_ema_period
    int - for: slow_ema_period

  Aiming to achieve all the parameters above, in a comma seperated list of 5
