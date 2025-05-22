from flask import Flask, jsonify
from simple_salesforce import Salesforce
from flask_cors import CORS
from collections import defaultdict
import logging
import os

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Salesforce-Verbindung herstellen
def connect_salesforce():
    """Establish a Salesforce connection using environment variables."""

    username = os.getenv("SALESFORCE_USERNAME")
    password = os.getenv("SALESFORCE_PASSWORD")
    security_token = os.getenv("SALESFORCE_SECURITY_TOKEN")

    if not all([username, password, security_token]):
        logging.error(
            "❌ Fehlende Salesforce-Zugangsdaten. Bitte Umgebungsvariablen setzen."
        )
        return None

    try:
        sf = Salesforce(
            username=username,
            password=password,
            security_token=security_token
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

    

@app.route('/accounts_by_landkreis')
def get_accounts_by_landkreis():
    sf = connect_salesforce()

    if sf is None:
        return jsonify({"error": "Keine Verbindung zu Salesforce möglich."}), 403

    query = """
        SELECT Id, Landkreis_Nummer__c
        FROM Account
        WHERE Landkreis_Nummer__c != NULL
        AND Status__c IN ('Mitglied', 'Mitglied in Kündigung')
    """

    try:
        landkreis_counts = defaultdict(int)
        result = sf.query(query)

        # erste Seite verarbeiten
        for record in result['records']:
            district = record.get('Landkreis_Nummer__c')
            if district:
                landkreis_counts[district] += 1

        # weitere Seiten (falls vorhanden)
        while not result['done']:
            result = sf.query_more(result['nextRecordsUrl'], True)
            for record in result['records']:
                district = record.get('Landkreis_Nummer__c')
                if district:
                    landkreis_counts[district] += 1

        logging.info("✅ Alle Accounts erfolgreich abgerufen und nach Landkreis aggregiert.")
        return jsonify(landkreis_counts)

    except Exception as e:
        logging.error(f"❌ Fehler bei Salesforce-Abfrage: {e}")
        return jsonify({"error": str(e)}), 403
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)

