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

  # 2 # Then use the example strategies given by Nautilus as first options
      See: nautilus_trader/examples/strategies
      See: condorgp/evaluation/naut_raw/blank_strat_n_strat_config.py

# <<<<<<<< HERE >>>>>>>>

      Then assemble working ADFs for 2 strategies (EMAcross and 2 others)
      Then work out how to bring them all into a strategy

      Q - need to understand the implications of adding >1 strategy

      Major game could be:
  # Allow EvolvedStrategy to:
        Select from a range of indicators
        Develop it's own logic as to how they are applied

      This means that the script that runs Nautilus is not evolved, many
      parts of it are unchanged.
        E.g condorgp/evaluation/naut_05_inject.py
        Has the following set:
          BacktestEngineConfig
          BacktestEngine
          Data configurations (in this case interest rate) and data for this
          Venue (trading venue - > 1 permitted)
          Instruments (in this case AUS v USD FX data)
          Wrangle and add data (in this case: audusd_ticks.csv)

          Evolved strategy added (we only change the EMACross fast and slow)

          Run reports
          Reset (basic but important)
          Dispose (basic but important)

# <<<<<<<< HERE >>>>>>>>

      A good deal of change is needed here

  # Evolving the strategy itself:


  # 3 # About indicators
      All indicators inherit base class Indicator, with Cython cimport

      from nautilus_trader.indicators.base.indicator cimport Indicator

      Question is - what do we evolve about indicators
        A - In the first instance, configure them to be added to strategies, or to be an ADF available to be used.
        Later: can get into evolving how an indicator works, or evolving new indicators.

# <<<<<<<< HERE >>>>>>>>

    NEXT - assemble working ADFs for 3 key indicators

    Initially, using the many indicators provided will be sufficient

    See long list of indicators:
      nautilus_trader/indicators

      grouped into
        other - in the folder above

        and a folder for each of
          averages
          base          a folder of the base classes etc
          fuzzy_enums
