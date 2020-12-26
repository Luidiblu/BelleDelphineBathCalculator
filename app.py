from dotenv import load_dotenv
from flask import Flask
import requests
import re
import os

'''
Avarage bathtub volume = 45 gallons (5760 fl oz) (170 litros)

Jar size = 8.5 fl oz (250 ml)

Belle Delphine weight = 55kg (1841 fl oz) (54 litros)

Bathtub Water = Bathtub Volume - Belle Delphine Volume = 3919 fl oz (115 litros)

Bathtub Water / Jar Size = 461 (Jars per bath)

Jar Price = $30

Money per Bath = Jar Price * Jars per bath = 13,830 USD (per bath)
'''

load_dotenv(verbose=True)

KEY = os.getenv('APIKEY')
app = Flask(__name__)

@app.route('/')
def hello():
    return transform_html()


def get_currency():
    updates_currency = {}
    print(KEY)
    r = requests.get(f'http://data.fixer.io/api/latest?access_key={KEY}&format=1')
    for money, value in r.json()['rates'].items():
        updates_currency[money] = value
    return updates_currency


def convert_money_per_bath():
    updates_currency = get_currency()
    converted_dict = {}
    converted_dict['USD'] = 13830
    for money, value in updates_currency.items():
        converted_dict[money] = (value * 13830)

    return converted_dict 

def clean_money():
    converted_dict = convert_money_per_bath()
    cleaned_dict = {}
    pattern = r".*\b.{2}"
    for money, value in converted_dict.items():
        value = str(value)
        new_value = re.match(pattern, value)
        cleaned_dict[money] = new_value.group()
    
    return cleaned_dict

def transform_html():
    cleaned_dict = clean_money()
    html = '''
    <style>
        .centered {
            position: absolute;
            top: 75%;
            left: 50%;
            transform: translate(-50%, -50%);
        }https://i.pinimg.com/originals/41/c4/8e/41c48e684eb7e2a99190e3d00bc77023.gif
    </style>
    <body style="background-image: url('https://i.pinimg.com/originals/41/c4/8e/41c48e684eb7e2a99190e3d00bc77023.gif')">
    <title>Belle Delphine Bath Calculator</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <img style="top:0; left:0; max-width:40vw" src="https://s9.limitedrun.com/images/1458913/unnamed.gif">
        <div class="container" style="padding-bottom: 25px;">
            <img style="width: 100%" src="https://wallpapercave.com/wp/wp6751479.jpg">
            <div class="centered">
                <img src="https://media.tenor.com/images/87c8bcd7c04d8f25701406bbe948adf3/tenor.gif">
            </div>
        </div>
        <div class="container">
            <div class="row">
    '''
    for money, value in cleaned_dict.items():
        html = html + f'''
            <div class="col-md-4 col-sm-6 text-center" style="padding-bottom: 25px;">
                <div style="background-color: white; border-radius: 15%">
                    <h1>
                        {money}
                    </h1>
                    <h2>
                        {value}
                    </h2>
                </div>
            </div>
        '''
    html = html + f'''</div> </div></body>'''

    return html

print(transform_html())