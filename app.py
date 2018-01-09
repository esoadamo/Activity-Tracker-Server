from flask import Flask, render_template, request, session, redirect, url_for, escape, request
from flask_sqlalchemy import SQLAlchemy
from os.path import isfile
import random
import string
import json

file_secrets = "secrets.conf"  # generated file with all secrets


app = Flask(__name__)
app.secret_key = ''
password_hash_salt = ''


# Initialization part of the script, together with first set-up
if not isfile(file_secrets):
    print('Now, generating your secrets...')
    password_hash_salt = ''.join(random.SystemRandom().choice(string.printable) for _ in range(64))
    app.secret_key = ''.join(random.SystemRandom().choice(string.printable) for _ in range(64))
    data_dict = {'password_hash_salt': password_hash_salt, 'app_secret': app.secret_key}
    with open(file_secrets, 'wt') as f:
        json.dump(data_dict, f, indent=1)
else:
    with open(file_secrets, 'rt') as f:
        data_dict = json.load(f)
        password_hash_salt = data_dict['password_hash_salt']
        app.secret_key = data_dict['app_secret']

print("That's all, your're clear for launch")
