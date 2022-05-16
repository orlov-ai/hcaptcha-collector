import os
import sys

from flask import *
from flask_hcaptcha import hCaptcha

app = Flask(__name__)
if ('HCAPTCHA_SITEKEY' not in os.environ) or ('HCAPTCHA_SECRETKEY' not in os.environ):
    print('Please set HCAPTCHA_SITEKEY and HCAPTCHA_SECRETKEY environment variables. Please look at README.md')
    sys.exit(1)
hcaptcha = hCaptcha(app,
                    site_key=os.environ['HCAPTCHA_SITEKEY'],
                    secret_key=os.environ['HCAPTCHA_SECRETKEY'],
                    is_enabled=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Create empty message
    if request.method == 'POST':  # Check to see if flask.request.method is POST
        if hcaptcha.verify():  # Use verify() method to see if hCaptcha is filled out
            message = 'Thanks for filling out the form!'  # Send success message
        else:
            message = 'Please fill out the hCaptcha!'  # Send error message
    return render_template('index.html', message=message, hcaptcha=hcaptcha.get_code())


if __name__ == '__main__':
    app.run(port=5000, host='test.mydomain.com')
