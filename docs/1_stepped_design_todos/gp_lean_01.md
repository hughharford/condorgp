# AIM: track next features, and what to test

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## REQUIREMENTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  # demonstrate decoupling
      # decouple deap_condor from Lean
      # decouple lean_runner from deap_condor
      # ENSURE deap_condor decoupled by design from ecosystem etc
      # LIKELY implement: https://github.com/ets-labs/python-dependency-injector
      # keep it super simple in the immediate term

  # gets fitness from lean
      # working fitness result (lean)
          # TODO: test to check deap runs lean and gets fitness

  # setup gp structure to run effectively with lean
      # TODO: test that required functionality provided in lean-evaluated class
      # TODO: test that run is successful

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
