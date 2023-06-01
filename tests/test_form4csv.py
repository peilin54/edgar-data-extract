import pytest
import os
import filecmp
from pathlib import Path
from edgar import run_form4


#  python main.py  -i ./tests/test_1 -o ./scratch
def test_1(tmp_path):
    input_path  = Path("./tests/test_1")
    output_path = tmp_path / "test_1"
    output_path.mkdir()
    run_form4(input_path, output_path, False)

    nd = 'nonDerivative.csv'
    d = 'derivative.csv'
    assert filecmp.cmp(str(output_path / nd), str(input_path / nd), shallow=False)
    assert filecmp.cmp(str(output_path / d), str(input_path / d), shallow=False)

  
# python main.py  -i ./tests/test_100 -o ./scratch -l True
def test_100(tmp_path):
    input_path  = Path("./tests/test_100")
    output_path = tmp_path / "test_100"
    output_path.mkdir()
    run_form4(input_path, output_path, True)

    nd = 'nonDerivative.csv'
    d = 'derivative.csv'
    assert filecmp.cmp(str(output_path / nd), str(input_path / nd), shallow=False)
    assert filecmp.cmp(str(output_path / d), str(input_path / d), shallow=False)
   

