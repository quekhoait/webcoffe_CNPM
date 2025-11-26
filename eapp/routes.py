from flask import Flask, render_template
from eapp import app
from eapp.controllers import home

app.add_url_rule('/','index',home.home)

app.add_url_rule('/about-us','about-us',home.aboutUs)


