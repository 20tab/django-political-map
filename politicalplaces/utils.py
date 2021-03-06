from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
# ISO 3166-1 country names and codes adapted from http://opencountrycodes.appspot.com/python/
# country and continents lists taken from https://github.com/20tab/twentytab-utils/blob/master/twentytab/countries.py

CONTINENTS = [
    ('africa', _('Africa')),
    ('antarctica', _('Antarctica')),
    ('asia', _('Asia')),
    ('europe', _('Europe')),
    ('north-america', _('North America')),
    ('oceania', _('Oceania')),
    ('south-america', _('South America')),
]

COUNTRIES = (
    ('AF', _('Afghanistan')),
    ('AX', _('Aland Islands')),
    ('AL', _('Albania')),
    ('DZ', _('Algeria')),
    ('AS', _('American Samoa')),
    ('AD', _('Andorra')),
    ('AO', _('Angola')),
    ('AI', _('Anguilla')),
    ('AQ', _('Antarctica')),
    ('AG', _('Antigua and Barbuda')),
    ('AR', _('Argentina')),
    ('AM', _('Armenia')),
    ('AW', _('Aruba')),
    ('AU', _('Australia')),
    ('AT', _('Austria')),
    ('AZ', _('Azerbaijan')),
    ('BS', _('Bahamas')),
    ('BH', _('Bahrain')),
    ('BD', _('Bangladesh')),
    ('BB', _('Barbados')),
    ('BY', _('Belarus')),
    ('BE', _('Belgium')),
    ('BZ', _('Belize')),
    ('BJ', _('Benin')),
    ('BM', _('Bermuda')),
    ('BT', _('Bhutan')),
    ('BO', _('Bolivia')),
    ('BA', _('Bosnia and Herzegovina')),
    ('BW', _('Botswana')),
    ('BV', _('Bouvet Island')),
    ('BR', _('Brazil')),
    ('IO', _('British Indian Ocean Territory')),
    ('BN', _('Brunei Darussalam')),
    ('BN', _('Brunei')),
    ('BG', _('Bulgaria')),
    ('BF', _('Burkina Faso')),
    ('BI', _('Burundi')),
    ('KH', _('Cambodia')),
    ('CM', _('Cameroon')),
    ('CA', _('Canada')),
    ('CV', _('Cape Verde')),
    ('KY', _('Cayman Islands')),
    ('CF', _('Central African Republic')),
    ('TD', _('Chad')),
    ('CL', _('Chile')),
    ('CN', _('China')),
    ('CX', _('Christmas Island')),
    ('CC', _('Cocos (Keeling) Islands')),
    ('CC', _('Cocos Islands')),
    ('CO', _('Colombia')),
    ('KM', _('Comoros')),
    ('CG', _('Congo')),
    ('CD', _('Congo, The Democratic Republic of the')),
    ('CD', _('Democratic Republic of the Congo')),
    ('CK', _('Cook Islands')),
    ('CR', _('Costa Rica')),
    ('CI', _('Cote d\'Ivoire')),
    ('CI', _('C\u00F4te d\'Ivoire')),
    ('HR', _('Croatia')),
    ('CU', _('Cuba')),
    ('CY', _('Cyprus')),
    ('CZ', _('Czech Republic')),
    ('CZ', _('Czechia')),
    ('DK', _('Denmark')),
    ('DJ', _('Djibouti')),
    ('CD', _('DRC')),
    ('DM', _('Dominica')),
    ('DO', _('Dominican Republic')),
    ('EC', _('Ecuador')),
    ('EG', _('Egypt')),
    ('SV', _('El Salvador')),
    ('GQ', _('Equatorial Guinea')),
    ('ER', _('Eritrea')),
    ('EE', _('Estonia')),
    ('ET', _('Ethiopia')),
    ('FK', _('Falkland Islands (Malvinas)')),
    ('FO', _('Faroe Islands')),
    ('FJ', _('Fiji')),
    ('FI', _('Finland')),
    ('FR', _('France')),
    ('GF', _('French Guiana')),
    ('PF', _('French Polynesia')),
    ('TF', _('French Southern Territories')),
    ('GA', _('Gabon')),
    ('GM', _('Gambia')),
    ('GE', _('Georgia')),
    ('DE', _('Germany')),
    ('GH', _('Ghana')),
    ('GI', _('Gibraltar')),
    ('GR', _('Greece')),
    ('GL', _('Greenland')),
    ('GD', _('Grenada')),
    ('GP', _('Guadeloupe')),
    ('GU', _('Guam')),
    ('GT', _('Guatemala')),
    ('GG', _('Guernsey')),
    ('GN', _('Guinea')),
    ('GW', _('Guinea-Bissa')),
    ('GY', _('Guyana')),
    ('HT', _('Haiti')),
    ('HM', _('Heard Island and McDonald Islands')),
    ('VA', _('Holy See (Vatican City State)')),
    ('VA', _('Vatican City')),
    ('HN', _('Honduras')),
    ('HK', _('Hong Kong')),
    ('HU', _('Hungary')),
    ('IS', _('Iceland')),
    ('IN', _('India')),
    ('ID', _('Indonesia')),
    ('IR', _('Iran, Islamic Republic of')),
    ('IR', _('Iran')),
    ('IQ', _('Iraq')),
    ('IE', _('Ireland')),
    ('IM', _('Isle of Man')),
    ('IL', _('Israel')),
    ('IT', _('Italy')),
    ('CI', _('Ivory Coast')),
    ('JM', _('Jamaica')),
    ('JP', _('Japan')),
    ('JE', _('Jersey')),
    ('JO', _('Jordan')),
    ('KZ', _('Kazakhstan')),
    ('KE', _('Kenya')),
    ('KI', _('Kiribati')),
    ('KP', _('Korea, Democratic People\'s Republic of')),
    ('KR', _('Korea, Republic of')),
    ('KR', _('Korea')),
    ('KW', _('Kuwait')),
    ('KG', _('Kyrgyzstan')),
    ('LA', _('Lao People\'s Democratic Republic')),
    ('LA', _('Laos')),
    ('LV', _('Latvia')),
    ('LB', _('Lebanon')),
    ('LS', _('Lesotho')),
    ('LR', _('Liberia')),
    ('LY', _('Libyan Arab Jamahiriya')),
    ('LY', _('Libya')),
    ('LI', _('Liechtenstein')),
    ('LT', _('Lithuania')),
    ('LU', _('Luxembourg')),
    ('MO', _('Macao')),
    ('MK', _('Macedonia, The Former Yugoslav Republic of')),
    ('MK', _('Macedonia')),
    ('MG', _('Madagascar')),
    ('MW', _('Malawi')),
    ('MY', _('Malaysia')),
    ('MV', _('Maldives')),
    ('ML', _('Mali')),
    ('MT', _('Malta')),
    ('MH', _('Marshall Islands')),
    ('MQ', _('Martinique')),
    ('MR', _('Mauritania')),
    ('MU', _('Mauritius')),
    ('YT', _('Mayotte')),
    ('MX', _('Mexico')),
    ('FM', _('Micronesia, Federated States of')),
    ('FM', _('Micronesia')),
    ('MD', _('Moldova')),
    ('MC', _('Monaco')),
    ('MN', _('Mongolia')),
    ('ME', _('Montenegro')),
    ('MS', _('Montserrat')),
    ('MA', _('Morocco')),
    ('MZ', _('Mozambique')),
    ('MM', _('Myanmar')),
    ('NA', _('Namibia')),
    ('NR', _('Naur')),
    ('NP', _('Nepal')),
    ('NL', _('Netherlands')),
    ('NL', _('The Netherlands')),
    ('AN', _('Netherlands Antilles')),
    ('NC', _('New Caledonia')),
    ('NZ', _('New Zealand')),
    ('NI', _('Nicaragua')),
    ('NE', _('Niger')),
    ('NG', _('Nigeria')),
    ('NU', _('Niue')),
    ('NF', _('Norfolk Island')),
    ('MP', _('Northern Mariana Islands')),
    ('KP', _('North Korea')),
    ('NO', _('Norway')),
    ('NO', _('Kingdom of Norway')),
    ('OM', _('Oman')),
    ('PK', _('Pakistan')),
    ('PW', _('Pala')),
    ('PS', _('Palestinian Territory, Occupied')),
    ('PA', _('Panama')),
    ('PG', _('Papua New Guinea')),
    ('PY', _('Paraguay')),
    ('PE', _('Per')),
    ('PH', _('Philippines')),
    ('PN', _('Pitcairn')),
    ('PN', _('Pitcairn Islands')),
    ('PL', _('Poland')),
    ('PT', _('Portugal')),
    ('PR', _('Puerto Rico')),
    ('QA', _('Qatar')),
    ('RE', _('Reunion')),
    ('RO', _('Romania')),
    ('RU', _('Russian Federation')),
    ('RU', _('Russia')),
    ('RW', _('Rwanda')),
    ('BL', _('Saint Barthelemy')),
    ('SH', _('Saint Helena')),
    ('KN', _('Saint Kitts and Nevis')),
    ('LC', _('Saint Lucia')),
    ('MF', _('Saint Martin')),
    ('PM', _('Saint Pierre and Miquelon')),
    ('VC', _('Saint Vincent and the Grenadines')),
    ('WS', _('Samoa')),
    ('SM', _('San Marino')),
    ('ST', _('Sao Tome and Principe')),
    ('ST', _('S\u00E3o Tom\u00E9 and Pr\u00EDncipe')),
    ('SA', _('Saudi Arabia')),
    ('SN', _('Senegal')),
    ('RS', _('Serbia')),
    ('SC', _('Seychelles')),
    ('SL', _('Sierra Leone')),
    ('SG', _('Singapore')),
    ('SK', _('Slovakia')),
    ('SI', _('Slovenia')),
    ('SB', _('Solomon Islands')),
    ('SO', _('Somalia')),
    ('ZA', _('South Africa')),
    ('GS', _('South Georgia and the South Sandwich Islands')),
    ('KR', _('South Korea')),
    ('ES', _('Spain')),
    ('LK', _('Sri Lanka')),
    ('SD', _('Sudan')),
    ('SR', _('Suriname')),
    ('SJ', _('Svalbard and Jan Mayen')),
    ('SZ', _('Swaziland')),
    ('SE', _('Sweden')),
    ('CH', _('Switzerland')),
    ('SY', _('Syrian Arab Republic')),
    ('SY', _('Syria')),
    ('TW', _('Taiwan, Province of China')),
    ('TW', _('Taiwan')),
    ('TJ', _('Tajikistan')),
    ('TZ', _('Tanzania, United Republic of')),
    ('TZ', _('Tanzania')),
    ('TH', _('Thailand')),
    ('TL', _('Timor-Leste')),
    ('TG', _('Togo')),
    ('TK', _('Tokela')),
    ('TO', _('Tonga')),
    ('TT', _('Trinidad and Tobago')),
    ('TN', _('Tunisia')),
    ('TR', _('Turkey')),
    ('TM', _('Turkmenistan')),
    ('TC', _('Turks and Caicos Islands')),
    ('TV', _('Tuval')),
    ('UG', _('Uganda')),
    ('UA', _('Ukraine')),
    ('AE', _('United Arab Emirates')),
    ('US', _('United States')),
    ('GB', _('United Kingdom')),
    ('UK', _('United Kingdom')),
    ('UM', _('United States Minor Outlying Islands')),
    ('UY', _('Uruguay')),
    ('UZ', _('Uzbekistan')),
    ('VU', _('Vanuat')),
    ('VE', _('Venezuela')),
    ('VN', _('Vietnam')),
    ('VG', _('Virgin Islands, British')),
    ('VI', _('Virgin Islands, U.S.')),
    ('WF', _('Wallis and Futuna')),
    ('EH', _('Western Sahara')),
    ('YE', _('Yemen')),
    ('ZM', _('Zambia')),
    ('ZW', _('Zimbabwe')),
)

CONTINENT_COUNTRIES = (
    (_('Africa'), (
        ('DZ', _('Algeria')),
        ('AO', _('Angola')),
        ('BJ', _('Benin')),
        ('BW', _('Botswana')),
        ('BF', _('Burkina Faso')),
        ('BI', _('Burundi')),
        ('CM', _('Cameroon')),
        ('CV', _('Cape Verde')),
        ('CF', _('Central African Republic')),
        ('TD', _('Chad')),
        ('KM', _('Comoros')),
        ('CG', _('Congo')),
        ('CD', _('Congo, The Democratic Republic of the')),
        ('CD', _('Democratic Republic of the Congo')),
        ('CD', _('DRC')),
        ('CI', _('Cote d\'Ivoire')),
        ('CI', _('C\u00F4te d\'Ivoire')),
        ('CI', _('Ivory Coast')),
        ('DJ', _('Djibouti')),
        ('EG', _('Egypt')),
        ('GQ', _('Equatorial Guinea')),
        ('ER', _('Eritrea')),
        ('ET', _('Ethiopia')),
        ('GA', _('Gabon')),
        ('GM', _('Gambia')),
        ('GH', _('Ghana')),
        ('GN', _('Guinea')),
        ('GW', _('Guinea-Bissa')),
        ('KE', _('Kenya')),
        ('LS', _('Lesotho')),
        ('LR', _('Liberia')),
        ('LY', _('Libyan Arab Jamahiriya')),
        ('LY', _('Libya')),
        ('MG', _('Madagascar')),
        ('YT', _('Mayotte')),
        ('MW', _('Malawi')),
        ('ML', _('Mali')),
        ('MR', _('Mauritania')),
        ('MU', _('Mauritius')),
        ('MA', _('Morocco')),
        ('MZ', _('Mozambique')),
        ('NA', _('Namibia')),
        ('NE', _('Niger')),
        ('NG', _('Nigeria')),
        ('RE', _('Reunion')),
        ('RW', _('Rwanda')),
        ('SH', _('Saint Helena')),
        ('ST', _('Sao Tome and Principe')),
        ('ST', _('S\u00E3o Tom\u00E9 and Pr\u00EDncipe')),
        ('SN', _('Senegal')),
        ('SC', _('Seychelles')),
        ('SL', _('Sierra Leone')),
        ('SO', _('Somalia')),
        ('ZA', _('South Africa')),
        ('SD', _('Sudan')),
        ('SZ', _('Swaziland')),
        ('TZ', _('Tanzania, United Republic of')),
        ('TZ', _('Tanzania')),
        ('TG', _('Togo')),
        ('TN', _('Tunisia')),
        ('UG', _('Uganda')),
        ('EH', _('Western Sahara')),
        ('ZM', _('Zambia')),
        ('ZW', _('Zimbabwe')),
    )),
    (_('Antarctica'), (
        ('AQ', _('Antarctica')),
        ('BV', _('Bouvet Island')),
        ('TF', _('French Southern Territories')),
        ('HM', _('Heard Island and McDonald Islands')),
    )),
    (_('Asia'), (
        ('AF', _('Afghanistan')),
        ('BH', _('Bahrain')),
        ('BD', _('Bangladesh')),
        ('BT', _('Bhutan')),
        ('IO', _('British Indian Ocean Territory')),
        ('BN', _('Brunei Darussalam')),
        ('BN', _('Brunei')),
        ('KH', _('Cambodia')),
        ('CN', _('China')),
        ('HK', _('Hong Kong')),
        ('IR', _('Iran, Islamic Republic of')),
        ('IR', _('Iran')),
        ('IN', _('India')),
        ('ID', _('Indonesia')),
        ('IQ', _('Iraq')),
        ('IL', _('Israel')),
        ('JP', _('Japan')),
        ('JO', _('Jordan')),
        ('KZ', _('Kazakhstan')),
        ('KW', _('Kuwait')),
        ('KP', _('Korea, Democratic People\'s Republic of')),
        ('KR', _('Korea, Republic of')),
        ('KR', _('Korea')),
        ('KP', _('North Korea')),
        ('KR', _('South Korea')),
        ('LA', _('Lao People\'s Democratic Republic')),
        ('LA', _('Laos')),
        ('KG', _('Kyrgyzstan')),
        ('LB', _('Lebanon')),
        ('MO', _('Macao')),
        ('MY', _('Malaysia')),
        ('MV', _('Maldives')),
        ('MM', _('Myanmar')),
        ('MN', _('Mongolia')),
        ('NP', _('Nepal')),
        ('OM', _('Oman')),
        ('PK', _('Pakistan')),
        ('PS', _('Palestinian Territory, Occupied')),
        ('PH', _('Philippines')),
        ('QA', _('Qatar')),
        ('RU', _('Russian Federation')),
        ('RU', _('Russia')),
        ('SA', _('Saudi Arabia')),
        ('SG', _('Singapore')),
        ('SY', _('Syrian Arab Republic')),
        ('SY', _('Syria')),
        ('LK', _('Sri Lanka')),
        ('TJ', _('Tajikistan')),
        ('TW', _('Taiwan, Province of China')),
        ('TW', _('Taiwan')),
        ('TH', _('Thailand')),
        ('TL', _('Timor-Leste')),
        ('TR', _('Turkey')),
        ('TM', _('Turkmenistan')),
        ('AE', _('United Arab Emirates')),
        ('UZ', _('Uzbekistan')),
        ('VN', _('Vietnam')),
        ('YE', _('Yemen')),
    )),
    (_('Europe'), (
        ('AX', _('Aland Islands')),
        ('AL', _('Albania')),
        ('AD', _('Andorra')),
        ('AM', _('Armenia')),
        ('AT', _('Austria')),
        ('AZ', _('Azerbaijan')),
        ('BY', _('Belarus')),
        ('BE', _('Belgium')),
        ('BA', _('Bosnia and Herzegovina')),
        ('BG', _('Bulgaria')),
        ('HR', _('Croatia')),
        ('CY', _('Cyprus')),
        ('CZ', _('Czech Republic')),
        ('CZ', _('Czechia')),
        ('DK', _('Denmark')),
        ('EE', _('Estonia')),
        ('FO', _('Faroe Islands')),
        ('FI', _('Finland')),
        ('FR', _('France')),
        ('GE', _('Georgia')),
        ('DE', _('Germany')),
        ('GI', _('Gibraltar')),
        ('GR', _('Greece')),
        ('GL', _('Greenland')),
        ('GG', _('Guernsey')),
        ('HU', _('Hungary')),
        ('IS', _('Iceland')),
        ('IE', _('Ireland')),
        ('IM', _('Isle of Man')),
        ('IT', _('Italy')),
        ('JE', _('Jersey')),
        ('LV', _('Latvia')),
        ('LI', _('Liechtenstein')),
        ('LT', _('Lithuania')),
        ('LU', _('Luxembourg')),
        ('MK', _('Macedonia, The Former Yugoslav Republic of')),
        ('MK', _('Macedonia')),
        ('MT', _('Malta')),
        ('MD', _('Moldova')),
        ('MC', _('Monaco')),
        ('ME', _('Montenegro')),
        ('NL', _('Netherlands')),
        ('NL', _('The Netherlands')),
        ('NO', _('Norway')),
        ('NO', _('Kingdom of Norway')),
        ('PL', _('Poland')),
        ('PT', _('Portugal')),
        ('RO', _('Romania')),
        ('SM', _('San Marino')),
        ('RS', _('Serbia')),
        ('SK', _('Slovakia')),
        ('SI', _('Slovenia')),
        ('ES', _('Spain')),
        ('SJ', _('Svalbard and Jan Mayen')),
        ('SE', _('Sweden')),
        ('CH', _('Switzerland')),
        ('UA', _('Ukraine')),
        ('GB', _('United Kingdom')),
        ('UK', _('United Kingdom')),
        ('VA', _('Holy See (Vatican City State)')),
        ('VA', _('Vatican City')),
    )),
    (_('North America'), (
        ('AS', _('American Samoa')),
        ('AI', _('Anguilla')),
        ('AG', _('Antigua and Barbuda')),
        ('AW', _('Aruba')),
        ('BS', _('Bahamas')),
        ('BB', _('Barbados')),
        ('BZ', _('Belize')),
        ('BM', _('Bermuda')),
        ('CA', _('Canada')),
        ('KY', _('Cayman Islands')),
        ('CR', _('Costa Rica')),
        ('CU', _('Cuba')),
        ('DM', _('Dominica')),
        ('DO', _('Dominican Republic')),
        ('SV', _('El Salvador')),
        ('GD', _('Grenada')),
        ('GP', _('Guadeloupe')),
        ('GT', _('Guatemala')),
        ('HT', _('Haiti')),
        ('HN', _('Honduras')),
        ('JM', _('Jamaica')),
        ('MX', _('Mexico')),
        ('MS', _('Montserrat')),
        ('AN', _('Netherlands Antilles')),
        ('NI', _('Nicaragua')),
        ('PA', _('Panama')),
        ('PR', _('Puerto Rico')),
        ('BL', _('Saint Barthelemy')),
        ('KN', _('Saint Kitts and Nevis')),
        ('LC', _('Saint Lucia')),
        ('MF', _('Saint Martin')),
        ('PM', _('Saint Pierre and Miquelon')),
        ('VC', _('Saint Vincent and the Grenadines')),
        ('TT', _('Trinidad and Tobago')),
        ('TC', _('Turks and Caicos Islands')),
        ('US', _('United States')),
        ('UM', _('United States Minor Outlying Islands')),
        ('VG', _('Virgin Islands, British')),
        ('VI', _('Virgin Islands, U.S.')),
    )),
    (_('Oceania'), (
        ('AU', _('Australia')),
        ('CX', _('Christmas Island')),
        ('CC', _('Cocos (Keeling) Islands')),
        ('CC', _('Cocos Islands')),
        ('CK', _('Cook Islands')),
        ('FJ', _('Fiji')),
        ('PF', _('French Polynesia')),
        ('GU', _('Guam')),
        ('KI', _('Kiribati')),
        ('MH', _('Marshall Islands')),
        ('FM', _('Micronesia, Federated States of')),
        ('FM', _('Micronesia')),
        ('NR', _('Naur')),
        ('NC', _('New Caledonia')),
        ('NZ', _('New Zealand')),
        ('NU', _('Niue')),
        ('NF', _('Norfolk Island')),
        ('MP', _('Northern Mariana Islands')),
        ('PW', _('Pala')),
        ('PG', _('Papua New Guinea')),
        ('PN', _('Pitcairn')),
        ('PN', _('Pitcairn Islands')),
        ('WS', _('Samoa')),
        ('SB', _('Solomon Islands')),
        ('TK', _('Tokela')),
        ('TO', _('Tonga')),
        ('TV', _('Tuval')),
        ('VU', _('Vanuat')),
        ('WF', _('Wallis and Futuna')),
    )),
    (_('South America'), (
        ('AR', _('Argentina')),
        ('BO', _('Bolivia')),
        ('BR', _('Brazil')),
        ('CL', _('Chile')),
        ('CO', _('Colombia')),
        ('EC', _('Ecuador')),
        ('FK', _('Falkland Islands (Malvinas)')),
        ('GF', _('French Guiana')),
        ('GY', _('Guyana')),
        ('MQ', _('Martinique')),
        ('PY', _('Paraguay')),
        ('PE', _('Peru')),
        ('GS', _('South Georgia and the South Sandwich Islands')),
        ('SR', _('Suriname')),
        ('UY', _('Uruguay')),
        ('VE', _('Venezuela')),
    )
    ),
)


def country_to_continent(country):
    for (continent, ctuple) in CONTINENT_COUNTRIES:
        its_countries = [cntry for code, cntry in ctuple]
        if country in its_countries:
            return continent
    return None
