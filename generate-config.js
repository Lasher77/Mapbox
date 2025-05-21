const fs = require('fs');
const token = process.env.MAPBOX_TOKEN;

if (!token) {
  console.error('MAPBOX_TOKEN environment variable is not set.');
  process.exit(1);
}

fs.writeFileSync('config.js', `window.config = {\n    MAPBOX_TOKEN: '${token}'\n};\n`);
console.log('config.js generated');
