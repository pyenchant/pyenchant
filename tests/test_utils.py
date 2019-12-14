from enchant.utils import trim_suggestions


def test_trim_suggestions():
    word = "gud"
    suggs = ["good", "god", "bad+"]
    assert trim_suggestions(word, suggs, 40) == ["god", "good", "bad+"]
    assert trim_suggestions(word, suggs, 4) == ["god", "good", "bad+"]
    assert trim_suggestions(word, suggs, 3) == ["god", "good", "bad+"]
    assert trim_suggestions(word, suggs, 2) == ["god", "good"]
    assert trim_suggestions(word, suggs, 1) == ["god"]
    assert trim_suggestions(word, suggs, 0) == []
