
from src.NOW.CodeSignal import c001_add

class TestOurFirstOne():
    
    def test_firstThing(self):
        a = 5
        b = 3
        assert a + b == c001_add.solution(a,b)