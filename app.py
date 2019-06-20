from flask import Flask, render_template, make_response
import pdfkit, json
import urllib.parse
import requests
import datetime
from functools import wraps, update_wrapper
import helper

app = Flask(__name__)

baseUrl = helper.apiUrl


@app.route('/')
def index():
    return 'Welcome to flask pdf'


@app.route('/blood/<blood>')
def employee_list(blood):
    query_text_orginal = blood
    query_text = urllib.parse.quote(query_text_orginal)
    user_detail = requests.get(baseUrl + '/blood-group-search?blood_group={0}'.format(query_text)).content
    user_detail = json.loads(user_detail)
    rendered = render_template('pdf_template.html', all_employee=None)
    if user_detail['code'] == 200:
        rendered = render_template('pdf_template.html', all_employee=user_detail)

        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        pdf = pdfkit.from_string(rendered, False, configuration=config)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=blood.pdf'
        return response
    return rendered


if __name__ == '__main__':
    app.run(debug=True)