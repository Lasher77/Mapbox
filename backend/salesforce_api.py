from flask import Flask, jsonify, request
from simple_salesforce import Salesforce
from flask_cors import CORS, cross_origin
from collections import defaultdict
import json
import logging
import os
from db import get_connection

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)
db_conn = get_connection()

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


@app.route('/mitarbeiter_by_landkreis')
def get_mitarbeiter_by_landkreis():
    sf = connect_salesforce()

    if sf is None:
        return jsonify({"error": "Keine Verbindung zu Salesforce möglich."}), 403

    query = """
        SELECT Landkreis_Code__c, Vorname__c, Name__c
        FROM Zuordnung_BV_auf_Landkreis__c
        WHERE Landkreis_Code__c != NULL
    """

    try:
        landkreis_staff = defaultdict(list)
        result = sf.query(query)

        for record in result['records']:
            code = record.get('Landkreis_Code__c')
            first = record.get('Vorname__c') or ''
            last = record.get('Name__c') or ''
            if code:
                landkreis_staff[code].append((first + " " + last).strip())

        while not result['done']:
            result = sf.query_more(result['nextRecordsUrl'], True)
            for record in result['records']:
                code = record.get('Landkreis_Code__c')
                first = record.get('Vorname__c') or ''
                last = record.get('Name__c') or ''
                if code:
                    landkreis_staff[code].append((first + " " + last).strip())

        logging.info("✅ Zuordnungen erfolgreich abgerufen und nach Landkreis gruppiert.")
        return jsonify(landkreis_staff)

    except Exception as e:
        logging.error(f"❌ Fehler bei Salesforce-Abfrage: {e}")
        return jsonify({"error": str(e)}), 403

@app.route('/unternehmen_by_landkreis')
def get_unternehmen_by_landkreis():
    """Return the total number of companies per district."""
    sf = connect_salesforce()

    if sf is None:
        return jsonify({"error": "Keine Verbindung zu Salesforce m\u00f6glich."}), 403

    query = """
        SELECT Landkreis_Nummer__c, Insgesamt_WZ2008_Abschnitte_B_NP_S__c
        FROM Potenziale_Lankreise__c
        WHERE Landkreis_Nummer__c != NULL
    """

    try:
        company_counts = {}
        result = sf.query(query)

        for record in result['records']:
            code = record.get('Landkreis_Nummer__c')
            count = record.get('Insgesamt_WZ2008_Abschnitte_B_NP_S__c')
            if code:
                company_counts[code] = count

        while not result['done']:
            result = sf.query_more(result['nextRecordsUrl'], True)
            for record in result['records']:
                code = record.get('Landkreis_Nummer__c')
                count = record.get('Insgesamt_WZ2008_Abschnitte_B_NP_S__c')
                if code:
                    company_counts[code] = count

        logging.info("✅ Unternehmenspotenziale erfolgreich abgerufen.")
        return jsonify(company_counts)

    except Exception as e:
        logging.error(f"❌ Fehler bei Salesforce-Abfrage: {e}")
        return jsonify({"error": str(e)}), 403


@app.route('/assignment/<rs>', methods=['GET'])
@cross_origin()
def get_assignment(rs):
    """Return stored assignment data for a district."""
    cur = db_conn.execute(
        "SELECT rs, wirtschaftsregion, fkt FROM assignments WHERE rs=?",
        (rs,)
    )
    row = cur.fetchone()
    if row is None:
        return jsonify({})
    return jsonify(
        {
            "rs": row["rs"],
            "wirtschaftsregion": row["wirtschaftsregion"],
            "fkt": json.loads(row["fkt"]) if row["fkt"] else [],
        }
    )


@app.route('/assignments', methods=['GET'])
@cross_origin()
def get_assignments():
    """Return a dict of all district codes that have an assignment."""
    cur = db_conn.execute("SELECT rs FROM assignments")
    data = {row["rs"]: True for row in cur.fetchall()}
    return jsonify(data)


@app.route('/assignment', methods=['POST'])
@cross_origin()
def post_assignment():
    """Store or update an assignment record."""
    data = request.get_json(force=True)
    rs = data.get("rs")
    region = data.get("wirtschaftsregion")
    fkt_list = data.get("fkt", [])
    if not rs:
        return jsonify({"error": "rs missing"}), 400
    db_conn.execute(
        "INSERT OR REPLACE INTO assignments(rs, wirtschaftsregion, fkt) VALUES (?, ?, ?)",
        (rs, region, json.dumps(fkt_list)),
    )
    db_conn.commit()
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # Listen on all interfaces so the API can be reached from other machines
    app.run(host='0.0.0.0', debug=True, port=5001)

