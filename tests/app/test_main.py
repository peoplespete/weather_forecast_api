'''Tests functions in defined in app/main.py'''
from app.main import pad_hour

def test_pad_hour():
    '''shows input and expected outputs for pad_hour function'''
    assert pad_hour('0') == '00'
    assert pad_hour('4') == '04'
    assert pad_hour('04') == '04'
    assert pad_hour('20') == '20'
