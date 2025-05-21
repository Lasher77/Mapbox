from flask import Flask, jsonify
from simple_salesforce import Salesforce
from flask_cors import CORS
from collections import defaultdict
import logging

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Salesforce-Verbindung herstellen
def connect_salesforce():
    try:
        sf = Salesforce(
	    username="sven.winkler-o1zh@force.com",
            password="BW-pfunkera69$",
            security_token="D57qFMPZ6jkpFkFKdWICbuuc"	
        )
        logging.info("✅ Verbindung zu Salesforce erfolgreich.")
        return sf
    except Exception as e:
        logging.error(f"❌ Fehler beim Verbinden zu Salesforce: {e}")
        return None

# Account-Daten abrufen
@app.route('/accounts')
def get_accounts():
    sf = connect_salesforce()

    if sf is None:
        return jsonify({"error": "Keine Verbindung zu Salesforce möglich."}), 403

    query = """
        SELECT Id, Name, BillingPostalCode, BillingCity, BillingState
        FROM Account
        WHERE BillingPostalCode != NULL
        
    """

    try:
        results = sf.query(query)['records']
        logging.info(f"✅ Abfrage erfolgreich: {len(results)} Datensätze.")
        return jsonify(results)
    except Exception as e:
        logging.error(f"❌ Fehler bei Salesforce-Abfrage: {e}")
        return jsonify({"error": str(e)}), 403

    

@app.route('/accounts_by_state')
def get_accounts_by_state():
    sf = connect_salesforce()

    if sf is None:
        return jsonify({"error": "Keine Verbindung zu Salesforce möglich."}), 403

    query = """
        SELECT Id, BillingState
        FROM Account
        WHERE BillingState != NULL
        AND Status__c IN ('Mitglied', 'Mitglied in Kündigung')
    """

    try:
        state_counts = defaultdict(int)
        result = sf.query(query)

        # erste Seite verarbeiten
        for record in result['records']:
            state = record['BillingState']
            state_counts[state] += 1

        # weitere Seiten (falls vorhanden)
        while not result['done']:
            result = sf.query_more(result['nextRecordsUrl'], True)
            for record in result['records']:
                state = record['BillingState']
                state_counts[state] += 1

        logging.info(f"✅ Alle Accounts erfolgreich abgerufen und aggregiert.")
        return jsonify(state_counts)

    except Exception as e:
        logging.error(f"❌ Fehler bei Salesforce-Abfrage: {e}")
        return jsonify({"error": str(e)}), 403
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)

