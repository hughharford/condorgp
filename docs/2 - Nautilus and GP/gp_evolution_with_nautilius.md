## Evolution expectations with Deap and Nautilus

  # 1 # Start small:
      Be able to set a population set and use it to run a configured strategy
      Using example EMAcross:

      See: condorgp/evaluation/nautilus/naut_runner_05_evolve_strategy_01.py

  # 1a # Ensure typed psets can handle ADFs effectively
    Try:
      A number of strategies added to the engine, each ADFs
      A range of indicators available for strategies

  # 2 # Then use the example strategies given by Nautilus as first options
      See: nautilus_trader/examples/strategies

  # 3 # Then consider implementing further reaching evolution,
      i.e. of a strategy itself

      The blank template is:
      condorgp/evaluation/naut_raw/blank_strat_n_strat_config.py
      Found in, and copied directly from:
      nautilus_trader/examples/strategies/blank.py

  # 4 # For this, using all the many indicators provided will
  # be likely sufficient

    See long list of indicators:
      nautilus_trader/indicators

      grouped into
        other - in the folder above

        and a folder for each of
          averages
          base
          fuzzy_enums
