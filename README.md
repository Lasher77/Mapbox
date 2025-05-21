# Mapbox

## Mapbox Token Setup

The frontend reads the Mapbox access token from a `config.js` file located in the project root. This file is ignored by git so that your token is not committed.

Create the file by copying `config.example.js` or by using the provided script:

```bash
# Option 1: copy the example and edit
cp config.example.js config.js
# then replace <YOUR_MAPBOX_TOKEN> with your token

# Option 2: generate from environment variable
MAPBOX_TOKEN=<your_token> node generate-config.js
```

After `config.js` is created, start the local server with:

```bash
python Server.py
```
