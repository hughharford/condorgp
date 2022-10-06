# FIRST PASS CREATING EVOLVABLE LEAN ALGO:

## Assumptions
  ### There are lots of moving parts that can be set to constant for now:
    # Execution Model:
      # There are a range of supported predefined models.
      # Some of them are listed here:
            self.SetExecution(NullExecutionModel())
                # doesn't really count

            self.SetExecution(ImmediateExecutionModel())

            self.SetExecution(SpreadExecutionModel())

            self.SetExecution(StandardDeviationExecutionModel())

      # For the Execution Model, we will set:
            self.SetExecution(ImmediateExecutionModel())
