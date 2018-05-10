# get distinct years of the Vod ,result in a list
# ['2014','20323',...]
from vodmanagement.models import Vod
from vodmanagement.utils import get_vod_field_list


def get_years(category):
    category = None if category == '全部' or category == '' else category
    _years = get_vod_field_list(Vod, 'year', category)
    years = []
    for year in _years:
        years.append(year[0])
    return years