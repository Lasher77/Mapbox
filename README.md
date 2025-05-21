# Mapbox


## Mapbox Token Setup

The frontend reads the Mapbox access token from a `config.js` file located in the project root. This file is ignored by git so that your token is not committed.

Create the file by copying `config.example.js` or by using the provided script:

# Option 1: copy the example and edit
cp config.example.js config.js
# then replace <YOUR_MAPBOX_TOKEN> with your token

# Option 2: generate from environment variable
MAPBOX_TOKEN=<your_token> node generate-config.js

After `config.js` is created, start the local server with:

python Server.py

=======
## Environment Variables

The backend connects to Salesforce and expects the credentials to be
available through environment variables:

- `SALESFORCE_USERNAME`
- `SALESFORCE_PASSWORD`
- `SALESFORCE_SECURITY_TOKEN`

You can create a `.env` file based on `.env.example` and load it before
running the API.

