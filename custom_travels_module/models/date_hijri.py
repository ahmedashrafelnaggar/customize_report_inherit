import math
# from odoo import models, fields
# from odoo.exceptions import UserError
from odoo import api, fields, models, _

STORE_HIJRI_ARABIC = True

HIJRI_MONTHS = [
    ('Muharram', 'Muharram'),
    ('Safar', 'Safar'),
    ('Rabi-I', 'Rabi-I'),
    ('Rabi-II', 'Rabi-II'),
    ('Jumada-I', 'Jumada-I'),
    ('Jumada-II', 'Jumada-II'),
    ('Rajab', 'Rajab'),
    ('Shaban', 'Shaban'),
    ('Ramadan', 'Ramadan'),
    ('Shawwal', 'Shawwal'),
    ('Dhul-Qadah', 'Dhul-Qadah'),
    ('Dhul-Hijjah', 'Dhul-Hijjah'),
]

if STORE_HIJRI_ARABIC:
    HIJRI_MONTHS = [
        ('Muharram', 'محرم'),
        ('Safar', 'صفر'),
        ('Rabi-I', 'ربيع الاول'),
        ('Rabi-II', 'ربيع الاخر'),
        ('Jumada-I', 'جمادي الاول'),
        ('Jumada-II', 'جمادي الاخر'),
        ('Rajab', 'رجب'),
        ('Shaban', 'شعبان'),
        ('Ramadan', 'رمضان'),
        ('Shawwal', 'شوال'),
        ('Dhul-Qadah', 'ذو القعده'),
        ('Dhul-Hijjah', 'ذو الحجة'),
    ]


def month_name_to_number(name):
    res = {
        'Muharram': '01',
        'Safar': '02',
        'Rabi-I': '03',
        'Rabi-II': '04',
        'Jumada-I': '05',
        'Jumada-II': '06',
        'Rajab': '07',
        'Shaban': '08',
        'Ramadan': '09',
        'Shawwal': '10',
        'Dhul-Qadah': '11',
        'Dhul-Hijjah': '12',

        'محرم': '01',
        'صفر': '02',
        'ربيع الاول': '03',
        'ربيع الاخر': '04',
        'جمادي الاول': '05',
        'جمادي الاخر': '06',
        'رجب': '07',
        'شعبان': '08',
        'رمضان': '09',
        'شوال': '10',
        'ذو القعده': '11',
        'ذو الحجة': '12',
    }[name]

    return int(res)


def month_number_to_name(number):
    res = list(map(lambda x: x[0], HIJRI_MONTHS))[number-1]
    if STORE_HIJRI_ARABIC:
        res = {
            1: 'محرم',
            2: 'صفر',
            3: 'ربيع الاول',
            4: 'ربيع الاخر',
            5: 'جمادي الاول',
            6: 'جمادي الاخر',
            7: 'رجب',
            8: 'شعبان',
            9: 'رمضان',
            10: 'شوال',
            11: 'ذو القعده',
            12: 'ذو الحجة',
        }[number]
    return res


def num_2_arabic(num):

    for en, ar in [
        ('0', '٠'),
        ('1', '١'),
        ('2', '٢'),
        ('3', '٣'),
        ('4', '٤'),
        ('5', '٥'),
        ('6', '٦'),
        ('7', '٧'),
        ('8', '٨'),
        ('9', '٩'),
    ]:
        num = str(num).replace(en, ar)
    return num


def arabic_2_num(num):

    for en, ar in [
        ('٠', '0'),
        ('١', '1'),
        ('٢', '2'),
        ('٣', '3'),
        ('٤', '4'),
        ('٥', '5'),
        ('٦', '6'),
        ('٧', '7'),
        ('٨', '8'),
        ('٩', '9'),
    ]:
        num = str(num).replace(en, ar)
    return num


def format_date(day, month, year):
    if STORE_HIJRI_ARABIC:

        day = num_2_arabic(day)
        year = num_2_arabic(year)
    return '%s/%s/%s' % (day, month, year)


def split_hijri(string_date):
    x = string_date.split('/')
    return {'day': x[0], 'month': x[1], 'year': x[2]}


def int_part(float_no):
    if float_no < -0.0000001:
        return math.ceil(float_no - 0.0000001)
    return math.floor(float_no + 0.0000001)


def hijri_to_gregorian(hijri):
    if not hijri:
        return False

    day = int(split_hijri(hijri)['day'])
    month = month_name_to_number(split_hijri(hijri)['month'])
    year = int(split_hijri(hijri)['year'])

    jd1 = int_part((11 * year + 3) / 30.0)
    jd2 = int_part((month - 1) / 2.0)
    jd = jd1 + 354 * year + 30 * month - jd2 + day + 1948440 - 385

    l = jd + 68569
    n = int_part((4 * l) / 146097.0)
    l = l - int_part((146097 * n + 3) / 4.0)
    i = int_part((4000 * (l + 1)) / 1461001.0)
    l = l - int_part((1461 * i) / 4.0) + 31
    j = int_part((80 * l) / 2447.0)
    d = l - int_part((2447 * j) / 80.0)
    l = int_part(j / 11.0)
    m = j + 2 - 12 * l
    y = 100 * (n - 49) + i + l

    return '%s-%s-%s' % (y, m, d)


def Gregorian2Hijri(gregorian):

    if not gregorian:
        return False

    gregorian = fields.Date.to_string(gregorian)

    year, month, day = map(lambda x: int(x), gregorian.split('-'))

    jd1 = int_part((1461 * (year + 4800 + int_part((month - 14) / 12.0))) / 4)
    jd2 = int_part((367 * (month - 2 - 12 * (int_part((month - 14) /
                                                  12.0)))) / 12)
    jd3 = int_part((3 * (int_part((year + 4900 + int_part((month - 14) /
                                                     12.0)) / 100))) / 4)
    jd = jd1 + jd2 - jd3 + day - 32075

    l = jd - 1948440 + 10632
    n = int_part((l - 1) / 10631.0)
    l = l - 10631 * n + 354

    j1 = (int_part((10985 - l) / 5316.0)) * (int_part((50 * l) / 17719.0))
    j2 = (int_part(l / 5670.0)) * (int_part((43 * l) / 15238.0))
    j = j1 + j2

    l1 = (int_part((30 - j) / 15.0)) * (int_part((17719 * j) / 50.0))
    l2 = (int_part(j / 16.0)) * (int_part((15238 * j) / 43.0))
    l = l - l1 - l2 + 29

    m = int_part((24 * l) / 709.0)
    y = 30 * n + j - 30
    d = l - int_part((709 * m) / 24.0)

    return y, m, d

DAYS = [(str(x).zfill(2), str(x).zfill(2)) for x in range(1, 31)]
if STORE_HIJRI_ARABIC:
    DAYS = [(str(x).zfill(2), num_2_arabic(str(x).zfill(2))) for x in range(1, 31)]

YEARS = [(str(x), str(x)) for x in range(1340, 1501)]
if STORE_HIJRI_ARABIC:
    YEARS = [(str(x), num_2_arabic(str(x))) for x in range(1340, 1501)]

class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def hijri2Gregorian(self):
        self.ensure_one()

        field_from = self._context['field_from']
        field_to = self._context['field_to']
        d = getattr(self, field_from)

        self.write({field_to: hijri_to_gregorian(d)})

    def Gregorian2hijri(self):
        self.ensure_one()

        field_from = self._context['field_from']
        field_to = self._context['field_to']
        d = getattr(self, field_from)
        if not d:
            self.write({field_to: False})
            return

        year, month, day = Gregorian2Hijri(d)
        hijri = format_date(day, month_number_to_name(month), year)

        self.write({field_to: hijri})

