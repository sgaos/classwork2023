import pytest

@pytest.mark.parametrize("HDL_input, expected",
[(65, "Normal"),
 (45, "Borderline Low"),
 (20, "Low")
 ])
def test_HDL_analysis(HDL_input, expected):
    from blood_calculator import HDL_analysis
    # Arrange
    # Act
    answer = HDL_analysis(HDL_input)
    # Assert
    assert answer == expected
 
 
@pytest.mark.parametrize("LDL_input, expected",
[(200, "Very High"),
 (170, "High"),
 (145, "Borderline High"),
 (20, "Normal")
 ])
def test_LDL_analysis(LDL_input, expected):
    from blood_calculator import LDL_analysis
    # Arrange
    # Act
    answer = LDL_analysis(LDL_input)
    # Assert
    assert answer == expected
 