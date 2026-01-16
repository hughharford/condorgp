import logging

class CellEvaluator():
# ''' defines fitness function for CondorGP Living Cell approach
#     and scores fitness when called based on current and changed
#     cell structures '''

    def __init__(self, scoring_name = None):
        ''' sets scoring_name, class structures.
            clean and simple.
        '''
        if scoring_name:
            self.scoring_name = scoring_name

        CellEvaluator.__extant_score_names = []

    @classmethod
    def get_all_for_score(cls):
        '''class method to return class type, e.g. CELL_TYPES'''
        if len(CellEvaluator.__extant_score_names) == 0:
            logging.debug("EMPTY: CellEvaluator.__extant_score_names is of length 0")
        return CellEvaluator.__extant_score_names

    @staticmethod
    def get_extant_score_names():
        '''static method retrieves single list of scoring_names'''
        if CellEvaluator.__extant_score_names == None:
            CellEvaluator.__extant_score_names = [] # create if not initialised
        return CellEvaluator.__extant_score_names

    def score_extant(self, scoring_name = None):
        ''' scoring heavy lifting:
            runs the cell_eval scoring in full
        '''
        if scoring_name is None:
            no_scored = self.score_all()
            return no_scored

        for cell in CellEvaluator.__extant_score_names:
            'run scoring for each'
            score_name, score = self.score_cell(cell)

    def score_cell(cell) -> tuple:
        pass
        return "scorename", 1.0
