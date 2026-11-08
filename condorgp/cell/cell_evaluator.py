import datetime
import logging

import cell

class CellEvaluator():
# ''' defines fitness function for CondorGP Living Cell approach
#     and scores fitness when called based on current and changed
#     cell structures '''

    def __init__(self, scoring_name = None, Cell = None, Cells = None):
        ''' sets scoring_name, class structures. clean and simple. '''
        CellEvaluator.__extant_score_names = []
        CellEvaluator.__extant_cells = []
        if scoring_name:
            self.scoring_name = scoring_name
            CellEvaluator.__extant_score_names.append(scoring_name)
        else:
            ''' TODO provide cover for scoring commands'''
            return "Scoring name or other command missing"
        if Cell:
            CellEvaluator.__extant_cells.append({
                                                "cell_naming": Cell.name,
                                                "detail": Cell.config_info,
                                                "date": datetime.datetime.now(),
                                                "score": 0.0
                                                })
            logging.debug(msg = "CellEvaluator added cell")
        elif Cells:
            pass


    @classmethod
    def get_all_for_score(cls):
        '''class method to return class type, e.g. CELL_TYPES'''
        return CellEvaluator.__extant_score_names

    @classmethod
    def confirm_score_name_extant(cls):
        ''' check via set that requested name there '''

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
            self.scoring_name = "None provided"
            no_scored = self.score_all()
            return no_scored

        for cell in CellEvaluator.__extant_score_names:
            ''' run scoring for every cell '''
            score_name, score = self.score_named(cell = cell)

    def score_all(self):
        ''' TODO score across all held cells, by scoring name'''
        pass

    def score_named(self, cell = None) -> tuple:
        if cell == None: return None, None
        return "scorename", 1.0
