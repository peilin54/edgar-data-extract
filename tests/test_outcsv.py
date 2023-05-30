import pytest
import os
import filecmp
from pathlib import Path
from edgar import run_form4


#  python main.py  -inpath ./tests/test_1 -outpath ./scratch
def test_1(tmp_path):
    inpath  = Path("./tests/test_1")
    outpath = tmp_path / "test_1"
    outpath.mkdir()
    run_form4(inpath, outpath, False)

    nd = 'nonDerivative.csv'
    d = 'derivative.csv'
    f = 'footnotes.csv'
    assert filecmp.cmp(str(outpath / nd), str(inpath / nd), shallow=False)
    assert filecmp.cmp(str(outpath / d), str(inpath / d), shallow=False)
    assert filecmp.cmp(str(outpath / f), str(inpath / f), shallow=False)

  
# python main.py  -inpath ./tests/test_100 -outpath ./scratch -readlist True
def test_100(tmp_path):
    inpath  = Path("./tests/test_100")
    outpath = tmp_path / "test_100"
    outpath.mkdir()
    run_form4(inpath, outpath, True)

    nd = 'nonDerivative.csv'
    d = 'derivative.csv'
    f = 'footnotes.csv'
    assert filecmp.cmp(str(outpath / nd), str(inpath / nd), shallow=False)
    assert filecmp.cmp(str(outpath / d), str(inpath / d), shallow=False)
    assert filecmp.cmp(str(outpath / f), str(inpath / f), shallow=False)
   

