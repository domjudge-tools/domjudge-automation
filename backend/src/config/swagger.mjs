import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import yaml from 'js-yaml';
import { config } from './index.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load YAML file
const yamlPath = path.join(__dirname, 'swagger.yaml');
const yamlContent = fs.readFileSync(yamlPath, 'utf8');

// Parse YAML to JavaScript object
const swaggerSpec = yaml.load(yamlContent);

// Update server URLs with dynamic port from config
swaggerSpec.servers = [
  {
    url: `http://localhost:${config.server.port}`,
    description: 'Development server (localhost)',
  },
  {
    url: `http://127.0.0.1:${config.server.port}`,
    description: 'Development server (127.0.0.1)',
  },
];

export { swaggerSpec };
