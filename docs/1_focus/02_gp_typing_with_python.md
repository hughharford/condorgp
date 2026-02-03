# working upwards, latest input at top of this file

  # STILL GETTING A RUST RELATED ERROR:
    '''Failed to set global default dispatcher because of error:
    a global default trace dispatcher has already been set'''

  # Sample challenge well on the way to being solved!

  # NEED TO SORT OUT THE "value has incorrect type" ERROR
      This has been fixed, adjusted pset below:

  # THIS WORKED:
    See copy of tightly controlled typed pset here:
    This isn't particularly elegant, but certainly shows typed control.
    Note the StrBar, StrInstr,BigInt & LittleInt (see class definitions below)
    - these aren't perfect - sometimes showing errors
    [E.g. Argument 'value' has incorrect type (expected str, got StrInstr)],
    but help contrain the degrees of freedom.

    def get_naut_pset_01(self):
        ''' naut_pset_01 '''
        bar_type = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        bar_type2 = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        bar_type3 = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"

        self.SIM = Venue("SIM")
        inst = TestInstrumentProvider.default_fx_ccy("AUD/USD", self.SIM)
        inst2 = TestInstrumentProvider.default_fx_ccy("AUD/USD",self.SIM)
        inst3 = TestInstrumentProvider.default_fx_ccy("AUD/USD",self.SIM)
        # print(f"type(instrument) = {type(instrument)}")
        # print(f"type(instrument.id) = {type(instrument.id)}")
        # print(f"type(str(instrument.id)) = {type(str(instrument.id))}")
        print(f"str(instrument.id) = {str(inst.id)}")

        # a first basic primitive set for strongly typed GP using Nautilus
        self.pset = gp.PrimitiveSetTyped("CGPNAUT01",
                                         [], EMACrossConfig, "ARG")

        # primary primitive, to enable function
        self.pset.addPrimitive(EMACrossConfig,
                               [StrInstr, StrBar, Decimal, LittleInt, BigInt],
                               EMACrossConfig)

        # first pset terminals:
        self.pset.addTerminal(StrInstr(inst.id), StrInstr)
        self.pset.addTerminal(StrInstr(inst2.id), StrInstr)
        self.pset.addTerminal(StrInstr(inst3.id), StrInstr)

        self.pset.addTerminal(bar_type, StrBar)
        self.pset.addTerminal(bar_type2, StrBar)
        self.pset.addTerminal(bar_type3, StrBar)

        self.pset.addTerminal(10, LittleInt)
        self.pset.addTerminal(20, LittleInt)
        self.pset.addTerminal(30, LittleInt)
        self.pset.addTerminal(40, LittleInt)
        self.pset.addTerminal(50, BigInt)
        self.pset.addTerminal(100, BigInt)
        self.pset.addTerminal(200, BigInt)
        self.pset.addTerminal(1_000_000, int)
        self.pset.addTerminal(2_000_000, int)

        # below here were added to allow DEAP to populate
        self.pset.addPrimitive(Decimal, [Decimal], Decimal)
        self.pset.addPrimitive(str, [str], str)
        self.pset.addPrimitive(int, [int], int)

        self.pset.addTerminal(Decimal(1_000_000), Decimal)
        self.pset.addTerminal("EMACrossConfig", EMACrossConfig)

        # using specified int and str classes to reduce degress of freedom
        self.pset.addPrimitive(BigInt, [BigInt], BigInt)
        self.pset.addPrimitive(LittleInt, [LittleInt], LittleInt)
        self.pset.addPrimitive(str, [StrInstr], StrInstr)
        self.pset.addPrimitive(str, [StrBar], StrBar)

        return self.pset

          # def get_config_strategy(self):
          #     config = EMACrossConfig(
          #         instrument_id=str(self.instrument.id),
          #         bar_type=self.bar_type,
          #         trade_size=Decimal(1_000_000),
          #         fast_ema_period=100,
          #         slow_ema_period=200,
          #         )
          #     return config

          # first attempt at Nautilus - looking to evolve the above

          class StrInstr(str):
              def pass_method(self):
                  pass

          class StrBar(str):
              def pass_method(self):
                  pass

          class BigInt(int):
              def pass_method(self):
                  pass

          class LittleInt(int):
              def pass_method(self):
                  pass

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

  # TRYING: Successful
  Calling the function without the explicit parameters.
    That works, so this is at least functional.

  ## Making it less explicit solves the issue immediately.
  Less explicitness could be countered by provided an explict name, so that
    for looking through the code, the "name output" is explicit and readable


  ## Explicit python declaration expects as above is difficult (trifficult):
  A parmeter for the function, bar_type is passed as:
    bar_type=input_variable_for_bar_type


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

# A key requirement is to provide strongly typed GP in Python
  This will allow specification for parameter inputs to functions etc
