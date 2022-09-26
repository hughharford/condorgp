# AIM: track next features, and what to test

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## REQUIREMENTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  # gets fitness from lean
      # working fitness result (lean)
          # TODO: test to check deap gets fitness

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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DONE
