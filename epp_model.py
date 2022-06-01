class Evaluator(list):
    """ A student that performed an evaluation during the peer review.
    An Evaluator is a list the contains the scores that this evaluator
    gave evaluated student. The scores apply to the evaluated student
    that possess this evaluator (see Evaluated class)
    Evaluator attributes are:
    - last_name: evaluator student's last name
    - surname:   evaluator student's surname
    - score:     average score given to the evaluated student normalized to 100 """
    
    def __init__(self, last_name: str, surname: str):
        super().__init__()
        self.last_name = last_name
        self.surname = surname
        self.score = 0.0
        
    def compute(self, min_scale: int, max_scale: int) -> float:
        total = 0.0
        
        # The following line is required to accomodate the way Moodle score data
        # is actually outputed by WorkshopETS "Export des evaluation (sans multiligne)".
        # The minimum aspect score is always 1. If a teacher wants the scale to start
        # from 0 (such as in ELE795), the min_scale parameter must be set to 0, and
        # then the program will substract 1 from all scores given by the evaluators.
        offset = 0.0 if min_scale == 1 else 1.0
        
        for note_aspect in self:
            total += note_aspect - offset
        self.score = total * 100.0 / (max_scale * len(self))
        return self.score
    
    def __repr__(self) -> str:
        x = super().__repr__()
        s = f"    Evaluator: {self.last_name}, {self.surname}, score={self.score:0.2f}, {x}\n"
        return s
    
    def append(self, value: int):
        if type(value) is int:
            super().append(value)
        else:
            raise TypeError("int expected")
    

class Evaluated(list):
    """ A student that was evaluated in a peer review.
    An Evaluated is a list of Evaluator.
    Evaluated attributes are:
    - last_name: evaluated student's last name
    - surname:   evaluated student's surname
    - email:     evaluated student's email
    - note:      average peer evaluation score given to this student
    - factor:    ratio of the evaluated student note over team average:
    
                          evaluated_student_note
                 factor = ----------------------
                              team average

                 This value normally ranges between 0.8 and 1.2.
                 It is meant to be multiplied with the homework note given
                 to the team by the teacher in order to obtain the final
                 evaluated student note.
    - modified:  boolean indicating if the student note was overridden
                 by an administrator with a manual input. In this case,
                 the note is note an average score, but the actual note
                 entered by the administrator.
                 
    compute_note() should be called after all teams have been added to EPP.
    compute_factor() should be called once the team average is known.
    compute_note() and compute_factor() are normally called by Team.compute(). """
    
    def __init__(self, last_name: str, surname: str, email: str):
        super().__init__()
        self.last_name = last_name
        self.surname = surname
        self.email = email
        self.modified = False
        self.note = 0.0
        self.factor = 0.0
        
    def compute_note(self, min_scale: int, max_scale: int) -> float:
        if self.modified:
            return self.note
        
        total = 0.0
        for e in self:
            total += e.compute(min_scale, max_scale)
        self.note = total / len(self)
        return self.note
    
    def compute_factor(self, average: float) -> None:
        self.factor = self.note / average
        
    def modify(self, note: float) -> None:
        self.note = note
        self.modified = True
                
    def __repr__(self) -> str:
        s = f"  Evaluated: {self.last_name}, {self.surname}, {self.email}, note={self.note:0.1f}, factor={self.factor:0.2f}, mod={self.modified}\n"
        for e in self:
            s += f"{e}"
        return s
    
    def append(self, e: Evaluator):
        if type(e) is Evaluator:
            super().append(e)
        else:
            raise TypeError("Evaluator expected")
        
        
class Team(list):
    """ Team is a student group among which a peer evaluation is done.
    A Team is a list of Evaluator.
    Team attributes are:
    - team_name: the team name
    - average:   average of all the Team evaluations
    compute() should be called after all teams have been added to EPP.
    Team.compute() is normaly called from EPP.compute(). """
    
    def __init__(self, team_name: str):
        super().__init__()
        self.name = team_name
        self.average = 0.0
        
    def compute(self, min_scale: int, max_scale: int) -> int:
        # compute evaluated students notes
        total = 0.0
        for e in self:
            total += e.compute_note(min_scale, max_scale)
            
        self.average = total / len(self)
        
        for e in self:
            e.compute_factor(self.average)
            
        return len(self)

    def __repr__(self) -> str:
        s = f"Team: {self.name}, average score={self.average:0.2f}\n"
        for e in self:
            s += f"{e}"
        return s
    
    def append(self, e: Evaluated):
        if type(e) is Evaluated:
            super().append(e)
        else:
            raise TypeError("Evaluated expected")


class EPP(list):
    """ EPP is the top structure of a peer evaluation ("Évaluation Par les Pairs").
    EPP is a list of Team.
    EEP attributes are:
    - groupings:   an array of n_evaluted booleans used separate Teams (for display)
    compute() should be called after all teams have been added to EPP.
    An EPP structure is normally populated by calling epp_reader.parse().
    
    A peer evaluation is done amongst a team of several students (normaly 4 or more).
    It is performed by students once homework has been hande over or a major milestone
    has been reached. In this process, each student evaluates its peer team member
    across several aspect (ex. quality of work, quantity of work done, leadership, etc.)
    The goal of this program is to compute a "factor" that is used to "modulate"
    the score given to the team for a homework.  That is, the factor should be
    multiplied with the team score in order to obtain the student score.
    For example, a student poorly evaluated during a peer review has a factor - 0.8.
    If the team's score for the homework is 80%, then the student score will be:
        student_score = 0.8 * 80 / 100 = 64%.
        
    min_scale and max_scale are respectively the minimm score and the maximum score
    that can be given to an aspect during the evaluation.  The min_scale should be
    0 or 1. The max scale is typically an integer value between 3 and 5 depending
    on the scale used. For example, the following scale:
        0 - inadequate
        1 - poor
        2 - average
        3 - good
        4 - excellent
    would lead to min_scale = 0 and max_scale = 4. """
    
    def __init__(self):
        super().__init__()
        self.groupings = []
        self.n_evaluated = 0
            
    def compute(self, min_scale: int, max_scale: int) -> None:
        self.n_evaluated = 0
        for t in self:
            self.n_evaluated += t.compute(min_scale, max_scale)
        self.create_groupings()
        # notify change here
        
    def create_groupings(self) -> None:
        self.groupings = []
        state = True
        
        for t in self:
            for _ in t:
                self.groupings.append(state)
            state = not state
                
    def __repr__(self) -> str:
        s =  f"Number of students evaluated: {self.n_evaluated}\n"
        s += f"Groupings: {self.groupings}\n"
        for t in self:
            s += f"{t}"
        return s
    
    def append(self, t: Team):
        if type(t) is Team:
            super().append(t)
        else:
            raise TypeError("Team expected")
