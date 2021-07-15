import nextOct as oct

def test_subdivide_range():
    assert oct.subdivide_range([0,8]) == [[0,4],[5,8]]
    assert oct.subdivide_range([0,9]) == [[0,4],[5,9]]
    assert oct.subdivide_range([3,6]) == [[3,4],[5,6]]
    assert oct.subdivide_range([3,7]) == [[3,5],[6,7]]