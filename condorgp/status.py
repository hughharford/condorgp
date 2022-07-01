

class Status():
    '''
    Class to run full suite of checks for cell population

    Updates or creates status data
    '''

    def __init__(self, cell_list, last_status=''):
        self.cell_list = cell_list
        if last_status != '':
            self.last_status = last_status

    def run_all_status_checks(self):
        '''
        This runs all the status checks
        Inputs the list of cells
        Returns the status of all cells
        '''
        pass

    def confirm_age_n_success(self):
        '''
        updates age, ranking and other stats based on recent
        progress
        includes
            > no. GP generations undertaken
            > no days/iterating trading
        '''
        pass

    def alive_or_dead(self):
        '''
        checks alive or dead status of cells
        based on
         > no of cells in the cell wall
         > ability to contribute drawdown
         > size expectations v ongoing stabilty (ratio tbc)
        '''
        pass

    def breeding_ready(self):
        '''
        checks against breeding criteria (tbc) and
        establishes if now is the moment to breed the succesful
        cell
        '''
        pass

    def trading_stats(self):
        '''
        pulls together from the cell record the overall
        trading numbers into a short set of key data.

        these key data will be used for graphics, comparison etc
        '''
        pass

    def draw_down_required(self):
        '''
        identifies the contribution taken from the cell,
        given the number days and trades made
        N.B. strict requirments for this not so well defined
        but key is that each cell's drawdown overall contributes
        to the success of the ecosystem financially, but shouldn't
        drain each cell too heavily
        '''
        pass
