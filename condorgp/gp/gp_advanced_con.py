from gp_control import GpControl



class GpAdvancedControl(GpControl):
    def __init__(self, pset_name=''):
        super().__init__()
        self.pop = 2
        self.ngen = 1
        self.default_pset_name = 'test_pset7aTyped'
        if pset_name:
            self.pset_name = pset_name
        else:
            self.pset_name = self.default_pset_name

    def setup(self, pset='', pop='', ngen=''):
        if pop: self.pop = pop
        if ngen: self.ngen = ngen
        self.setup_gp(pset, self.pop, self.ngen)

    def run_gp(self, inputs=...):
        return super().run_gp(inputs)

    def graph_progress(self):
        pass

if __name__ == "__main__":
    eval_used = 'eval_test_6'
    pset_used = 'test_pset8aTyped' # 'test_pset8aTyped'
    gp_ac = GpAdvancedControl()
    p = 2
    g = 1
    gp_ac.setup(pset_used, p, g)
    gp_ac.run_lean = 0
    gp_ac.default_tidyup = 0
    gp_ac.set_test_evaluator(eval_used)
    gp_ac.run_gp()
