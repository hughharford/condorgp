# AIM: track next features, and what to test

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## REQUIREMENTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  # setup gp structure to run effectively with lean
      # TODO: test that required functionality provided in lean-evaluated class
      # TODO: test that run is successful


  # enable strongly-typed deap gp
      # use strongly typed gp to control the tree

      # design and build the trunk and branches to structure the output
          @ might be simpler to evolve as many adfs or trees as required?
          @ the tree based structure gives a by-nature nested call approach

      # seems like the most simple approach will be to customise the gp algo
          @ run X different primitive sets, each for a line of code required

      # ADFs, surely?
          @ an adfset is just a PrimitiveSetTyped

      # Lean requires:


  # vary the individuals for fitness evaluation
      # ability to vary the individuals sent for fitness evaluation
          # TODO: test checking func provision to vary individuals



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



  # logging functioning as intended
      # logging to: /home/hsth/code/hughharford/condorgp/condorgp/util/logs/condor_log.txt
      # logging to localpackages/condorgp


  # ability to set, run, and restart a pickled population (checkpointing)
      # confirm can pickle
      # confirm can unpickle and run
    # REF: https://deap.readthedocs.io/en/master/tutorials/advanced/checkpoint.html

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DONE

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
