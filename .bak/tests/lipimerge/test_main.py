import pytest
import os
from lipimerge.__main__ import main
import lipimerge.internal.xutils as xutils

test_path = './tests/data/main'

@pytest.fixture
def pre_cleanup():
    """
    Cleanup before test.

    Do not clean up after test to allow inspection of test artifacts.
    """
    def delete_file(file_name):
        if os.path.exists(os.path.join(test_path, file_name)):
            os.remove(os.path.join(test_path, file_name))

    for file in ['lipimerge.xlsx', 'out/result-full.xlsx', 'out/result-2356.xlsx']: delete_file(file)
    
    yield


@pytest.mark.parametrize("args, out, expected", [
    (['-d', test_path], 'lipimerge.xlsx', 'expected/full_merge.xlsx'),
    (['-d', test_path, '-o', 'out/result-full.xlsx'], 'out/result-full.xlsx', 'expected/full_merge.xlsx'),
    (
        [
            f"{test_path}/data-2.xlsx",
            f"{test_path}/data-3.xlsx",
            f"{test_path}/other_dir/data-5.xlsx",
            f"{test_path}/other_dir/data-6.xlsx",
            '-o', f"{test_path}/out/result-2356.xlsx"
        ], 
        'out/result-2356.xlsx', 'expected/2356_merge.xlsx'
    ),
])
def test_main_merge_success(pre_cleanup, monkeypatch, args, out, expected):
    monkeypatch.setattr('sys.argv', ['lipimerge'] + args)
    result = main()
    assert result.errcode == 0
    assert os.path.exists(os.path.join(test_path, out))
    with xutils.workbook(os.path.join(test_path, out)) as out:
        with xutils.workbook(os.path.join(test_path, expected)) as exp:
            assert out.sheetnames == exp.sheetnames
            for sheetname in out.sheetnames:
                if sheetname == 'lipimerge.log': continue
                assert xutils.equal(out[sheetname], exp[sheetname])

