#!/usr/bin/env python
import connexion
import logging
from connexion.resolver import RestyResolver

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app = connexion.App(__name__)
    app.add_api('scaner_api.yaml', arguments={'title': 'Scaner\'s API'}, resolver=RestyResolver('scaner.controllers'))
    app.run(port=5000)
