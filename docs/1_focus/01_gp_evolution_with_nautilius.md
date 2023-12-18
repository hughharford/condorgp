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
        A - In the first instance, configure them to be added to strategies,
        or to be an ADF available to be used.
        B - Later: can get into evolving how an indicator works,
        or evolving new indicators.

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

    Select indicators to be ADFs:

    from nautilus_trader.indicators.average:
      1 _ WeightedMovingAverage(MovingAverage)
      2 _ AdaptiveMovingAverage(MovingAverage)
      3 _ VariableIndexDynamicAverage(MovingAverage)

    from nautilus_trader.indicators:
      4 _
      5 _

    THIS NEEDS SOME MORE THOUGHT - i.e. pick indicators that build together
    to enable the strategies

# <<<<<<<< HERE >>>>>>>>
# <<<<<<<< FOCUS HERE >>>>>>>>

    Additionally, need to understand how to wire these pieces together.

    1 - Read and understand Nautilus example strategies, looking for examples
    for where indicators are used. Aim: to understand their configuration and
    use - hopefully simple enough to be ADFs.
      (a) Starting here, from the top: nautilus_trader/examples/strategies

          nautilus_trader/examples/strategies/ema_cross_bracket_algo.py
          _____________________________________________________________

          from nautilus_trader.indicators.atr import AverageTrueRange
          from nautilus_trader.indicators.average.ema import ExponentialMovingAverage

          # in __init__, simply, with int config.set_variables:
          # Create the indicators for the strategy
          self.atr = AverageTrueRange(config.atr_period)
          self.fast_ema = ExponentialMovingAverage(config.fast_ema_period)
          self.slow_ema = ExponentialMovingAverage(config.slow_ema_period)

          # in on_start:
          # Register the indicators for updating
          self.register_indicator_for_bars(self.bar_type, self.atr)
          self.register_indicator_for_bars(self.bar_type, self.fast_ema)
          self.register_indicator_for_bars(self.bar_type, self.slow_ema)

          # given this uses bar data:
          # on_bar holds the buy and sell logic
          # buy and sell methods execute via call from on_bar
          # buy and sell methods include a 15 strong order_list

          nautilus_trader/examples/strategies/ema_cross_bracket.py
          ________________________________________________________

          # Only different to the algo above, in that the algo includes
          # lots of order management - this is for later.

          nautilus_trader/examples/strategies/ema_cross_stop_entry.py
          ___________________________________________________________

          # This shows examples of order types, rather than indicator use

          nautilus_trader/examples/strategies/ema_cross_trailing_stop.py
          ______________________________________________________________

          # Similar - trailing stop buy and sell in on_event method

    Interesting reading so far:
      The examples focus more on order types, which makes sense. These show
      some different approaches. All of which can be evolved, but not soon. 

# DESIGN DECISION REQUIRED
  # There will be lots of ADFs this way
      Indicators
        8 x moving average
       29 x indicators

      Not expected to be required:
        4 x fuzzy_enums - these are used in the fuzzy_candle stick indicator
