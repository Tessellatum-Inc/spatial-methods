import math
import pytest
from string_linkage import *


def test_normalization_and_edit_distance():
    assert normalize_text("  Café—Road,  NAIROBI ") == "café road nairobi"
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("", "") == 0
    assert normalized_levenshtein("", "") == 1
    assert normalized_levenshtein("abc", "xyz") == 0


def test_jaro_winkler_reference_values():
    assert jaro_winkler("MARTHA", "MARHTA") == pytest.approx(0.9611111111)
    assert jaro_winkler("DWAYNE", "DUANE") == pytest.approx(0.84)
    assert jaro_winkler("same", "same") == 1
    assert jaro_winkler("", "x") == 0
    with pytest.raises(ValueError): jaro_winkler("a", "b", 0.3)


def test_character_ngram_cosine():
    assert character_ngram_cosine("spatial", "spatial") == pytest.approx(1)
    assert 0 < character_ngram_cosine("spatial", "spat ial") < 1
    assert character_ngram_cosine("", "") == 1
    with pytest.raises(ValueError): character_ngram_cosine("a", "b", 0)


def test_soundex_examples():
    assert soundex("Robert") == "R163"
    assert soundex("Rupert") == "R163"
    assert soundex("Ashcraft") == "A261"
    assert soundex("") == ""


def test_prefix_blocking():
    rows = [{"name":"Nairobi Road"}, {"name":"Nairobi Rd"}, {"name":"Mombasa Road"}]
    assert exact_prefix_blocks(rows, "name", 4) == {"nair":[0,1], "momb":[2]}
    with pytest.raises(ValueError): exact_prefix_blocks(rows, "name", 0)


def test_canopy_pairs():
    rows = [{"name":"Nairobi"}, {"name":"Nairob"}, {"name":"Mombasa"}]
    assert (0,1) in canopy_pairs(rows, "name", 0.8, 0.95)
    with pytest.raises(ValueError): canopy_pairs(rows, "name", 0.8, 0.7)


def test_fellegi_sunter_weights():
    probs = {"name":(0.9,0.1), "postcode":(0.95,0.05)}
    score = fellegi_sunter_score({"name":True,"postcode":False}, probs)
    assert score == pytest.approx(math.log(9)+math.log(0.05/0.95))
    assert fellegi_sunter_score({"name":True},{"name":(0.9,0.1)}) > 0
    assert fellegi_sunter_score({"name":False},{"name":(0.9,0.1)}) < 0
    with pytest.raises(KeyError): fellegi_sunter_score({"x":True}, probs)
    with pytest.raises(ValueError): fellegi_sunter_score({"name":True},{"name":(1,0.1)})
