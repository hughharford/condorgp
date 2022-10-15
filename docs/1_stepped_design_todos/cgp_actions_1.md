# AIM: track next features, and what to test

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## REQUIREMENTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  # enable imports of Lean classes into Condorgp and vice versa
      # TODO: fix this, without it things are complex
      # OPTIONS:
          1. Fix both ways import
             1. condorgp imports of Lean (fails: DETAIL)
             2. Lean imports of condorgp (fails: algorithm wrapper error)
             3. NOTE: there might be a way to only run with 2 solved
          2. Port condorgp into Lean/LocalPackages
             1. deal with git interaction, two way thing Lean / condorgp

      # ACTION:
          a) read up about what Lean recommend, condorgp isn't the only project
            SUGGESTED: https://pypi.org/project/quantconnect-stubs/
                  install: pip install quantconnect-stubs
                  use: include in all py files: from AlgorithmImports import *
                  quantconnect-stubs already installed!
            FOUND in QUANTCONNECT/LEAN:
                  PythonToolbox
                      worth looking at...
                  Visualizer
                      also worth looking at:
                      /home/hsth/code/hughharford/Lean/ToolBox/Visualizer
          b) consider other backtesting and finance options

  # enable strongly-typed deap gp
      # DONE use first strongly typed gp to control the tree

      # design and build the trunk and branches to structure the output
          @ might be simpler to evolve as many adfs or trees as required?
          @ the tree based structure gives a by-nature nested call approach

      # seems like the most simple approach will be to customise the gp algo
          @ run X different primitive sets, each for a line of code required
          @ cancel this, see below ADFs

      # ADFs, surely?
          @ an adfset is just a PrimitiveSetTyped
          @ these can be evolved alongside, and be accessed via a simple list

      # TYPING REQUIREMENTS (given no import into Lean/LocalPackages yet):
          # copy a .py with all functions into Lean/LocalPackages
          # keep a dict: {'function_name':'replacement_string'}
          # the replacement_string transforms from
          #                     function name - e.g. 'double'
          #                     to
          #           referenced function name, e.g. 'cfs.double'
          #           where
          #           cfs is the object name for GpCustomFunctions


  # set up condorgp STGP with Lean features we can vary:
      # Lean requires / can feature:
            initialise
            alpha models
            on_data
            on_update (for stock changes)
            portfolio construction
            execution models
            risk management


  # Custom typing as part of strongly typed GP
      # see DEAP Custom Typing ___ in Firefox bookmarks under: DEAP
      #  primitive and a terminal for each type you defined, or else DEAP won't be able to generate arbitrarily shaped trees.
      # REF: https://groups.google.com/g/deap-users/c/NgL8_rYr4MI/m/-rg4LJJgAAAJ



  # shows +ve fitness change, using fitness max
      # enough variance in fitness evaluation to show +ve fitness change
      # TODO: test fitness increases > twice
          # TODO: test on start & end date (constant, long enough)

          # REDUCES
            # creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
            # creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)
          # OR INCREASES
            # creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
            # creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)
      # PROGRESS ON THIS:
          # see test_07
            # evaluator: eval_test_7 , and pset: test_pset7aTyped



  # logging functioning as intended
      # DONE: logging to: /home/hsth/code/hughharford/condorgp/condorgp/util/logs/condor_log.txt
      # TODO: logging to localpackages/condorgp


  # ability to set, run, and restart a pickled population (checkpointing)
      # confirm can pickle
      # confirm can unpickle and run
    # REF: https://deap.readthedocs.io/en/master/tutorials/advanced/checkpoint.html





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DONE

  # check through new gp_functions.get_fit_6
      # DONE Enough for now...

      # test_06 fails when it should pass...
      # this is not simple...
      # for a start:
          # the gp outcomes are not always the same
          # get_fit_6() now has logging to show where the fitness came from
      # test_06 definitely passes sometimes

  # build error catching into lean_runner
      # DONE: enable error checking from Lean logs
        # search for, see examples of:
            ERROR:: << CONDOR INJECT-CODE ERROR >>
      # DONE: report -99999 fitness when this happens
          see gp_functions.get_fit_6 and related

  # setup gp structure to run effectively with lean
      # DONE: test that required functionality provided in lean-evaluated class
      # DONE: test that run is successful
        # basic gp running is operational with Lean
        # see tests 04-06

  # vary the individuals for fitness evaluation
      # ability to vary the individuals sent for fitness evaluation
          # DONE: test checking func provision to vary individuals
          # see test_06 for Lean influence based on psets and individuals


  # get out the python code for each individual
      # DONE: simple enough, just:
              print('print of each individual might give code enough:\n')
              for ind in ccc.pop:
                  print(ind)

  # demonstrate decoupling
      # decouple deap from gp_control
          # DONE, see interfaces/gp_provider & inject_gp method
      # decouple lean_runner (and thereby Lean) from gp_control
          # DONE - see inject_lean_runner method
      # decouple utils from gp_control
          # DONE - see inject_utils method
      # ENSURE gp_control decoupled by design from ecosystem etc
      # CONSIDER implement: https://github.com/ets-labs/python-dependency-injector
      # keep it super simple in the immediate term
        # => manual DI, single factory
  # gets fitness from lean
      # working fitness result (lean)
          # DONE: test to check deap runs lean and gets fitness
            # see test_04_deap-runs_lean_steps.py
