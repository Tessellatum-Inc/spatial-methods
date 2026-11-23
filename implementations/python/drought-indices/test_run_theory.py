import pytest
from run_theory import run_theory_events

def test_below_threshold_events_and_severity():
    events=run_theory_events([0,-1,-2,0,-3,-1,1],-.5,direction="below",min_duration=2)
    assert len(events)==2
    assert events[0]=={"start":1,"end":2,"duration":2,"exceedance_days":2,"severity":2.0,"peak_severity":1.5,"mean_severity":1.0}

def test_gap_bridging_counts_calendar_duration_not_exceedance_days():
    events=run_theory_events([0,-2,0,-3,0],-1,max_gap=1,min_duration=2)
    assert len(events)==1 and events[0]["duration"]==3 and events[0]["exceedance_days"]==2
    assert events[0]["severity"]==3

def test_missing_values_always_break_events():
    events=run_theory_events([-2,float("nan"),-3],-1,max_gap=5)
    assert len(events)==2

def test_above_threshold_and_validation():
    event=run_theory_events([0,3,4,0],2,direction="above")[0]
    assert event["severity"]==3
    with pytest.raises(ValueError): run_theory_events([],0)
    with pytest.raises(ValueError): run_theory_events([1],0,direction="sideways")
    with pytest.raises(ValueError): run_theory_events([1],0,min_duration=0)
