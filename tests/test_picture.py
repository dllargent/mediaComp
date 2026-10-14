import pytest
from mediaComp import*

@pytest.mark.parametrize("w,h", [
    (300, 200),      # 正常中间值
    (1, 1),          # 边界值: 最小尺寸 (必须大于0，所以改成1,1)
    (10000, 10000)   # 边界值: 最大尺寸
])
def test_makeEmptyPicture_boundaries(w, h):
    pic = makeEmptyPicture(w, h)
    
    assert getWidth(pic) == w
    assert getHeight(pic) == h

def test_picture_catch_bug():
    pic = makeEmptyPicture(1317, 1123)
    
    assert getWidth(pic) == 1317
    assert getHeight(pic) == 1123

def test_makeEmptyPicture_negative_values():
    # 测试负数宽度，预期会抛出 ValueError
    with pytest.raises(ValueError):
        makeEmptyPicture(-100, 200)
        
    # 测试负数高度，预期会抛出 ValueError
    with pytest.raises(ValueError):
        makeEmptyPicture(100, -50)
