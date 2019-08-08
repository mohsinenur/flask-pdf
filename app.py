from flask import Flask, render_template, flash, make_response, request, redirect, jsonify, send_file
import pdfkit, json
import urllib.parse
import requests
import datetime
from functools import wraps, update_wrapper
import helper
from flask_weasyprint import HTML, render_pdf
from views import details_bank_report

app = Flask(__name__)
app.secret_key = 'super secret key'

baseUrl = helper.apiUrl
siteUrl = helper.siteUrl


@app.route('/')
def index():
    return 'Welcome to flask pdf'


@app.route('/bank-report-pdf', methods=['GET', 'POST'])
def bank_report_pdf():
    data = request.get_json(force=True)
    report_name = 'bank-report-' + str(datetime.datetime.now().strftime('%Y-%m-%d at %H-%M'))
    details_bank_report.detailsBankReport(data)
    rendered = render_template('bank_report_pdf.html', response=data)
    pdf_settings = {
        'page-size': 'Letter',
        'margin-top': '0.5in',
        'margin-right': '0.3in',
        'margin-bottom': '0.5in',
        'margin-left': '0.3in',
        'encoding': "UTF-8",
        'dpi': 70,
    }
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    pdf = pdfkit.from_string(rendered, output_path='./pdf/' + report_name + '.pdf', configuration=config, options=pdf_settings)

    # response = make_response(pdf)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'attachment; filename=bank-report.pdf'
    return '<a href="' + siteUrl + '/report-download/' + report_name + '.pdf">Download</a>'


@app.route('/report-download/<string:pdf>')
def report_download (pdf):
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "./pdf/" + pdf
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)