## Evolution expectations with Deap and Nautilus

  # 1 # Start small:
      Be able to set a population set and use it to run a configured strategy
      Using example EMAcross:

      See: condorgp/evaluation/nautilus/naut_runner_05_evolve_strategy_01.py

  # 1a # Ensure typed psets can handle ADFs effectively
    Try:
      A number of strategies added to the engine, each ADFs
      A range of indicators available for strategies

      DONE - gp_deap_adf and gp_deap_adf_cp both run with ADFs
        Starting with a very simple ADF addition to naut_pset_02_adf
        ADF evaluation looks very different based on the examples

# <<<<<<<< HERE >>>>>>>>

      NEXT - assemble working ADFs for 3 key indicators
      Then assemble working ADFs for 2 strategies (EMAcross and 2 others)
      Then work out how to bring them all into a strategy
        See: condorgp/evaluation/naut_raw/blank_strat_n_strat_config.py


  # 2 # Then use the example strategies given by Nautilus as first options
      See: nautilus_trader/examples/strategies

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
