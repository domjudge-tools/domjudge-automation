import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import swaggerUi from 'swagger-ui-express';
import { config } from './config/index.mjs';
import logger from './utils/logger.mjs';
import teamRoutes from './routes/teamRoutes.mjs';
import { errorHandler } from './middleware/errorHandler.mjs';
import { swaggerSpec } from './config/swagger.mjs';

const app = express();

// Middleware - Configure Helmet to allow Swagger UI
app.use(helmet({
  contentSecurityPolicy: false,
  crossOriginEmbedderPolicy: false,
}));

// CORS configuration - Allow all origins for Swagger UI
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization', 'Accept', 'X-Requested-With'],
  credentials: false,
}));

// Handle preflight requests
app.options('*', cors());

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Request logging (skip for Swagger UI assets)
app.use((req, res, next) => {
  // Skip logging for Swagger UI static files
  if (req.path.startsWith('/api-docs') && req.path !== '/api-docs.json') {
    return next();
  }
  logger.info(`${req.method} ${req.path}`, {
    ip: req.ip,
    userAgent: req.get('user-agent'),
  });
  next();
});

// Swagger JSON endpoint - Must be before Swagger UI setup
app.get('/api-docs.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.send(swaggerSpec);
});

// Swagger documentation UI - Fully interactive configuration
const swaggerUiOptions = {
  customCss: `
    .swagger-ui .topbar { display: none }
    .swagger-ui .btn.execute { 
      background-color: #49cc90 !important; 
      border-color: #49cc90 !important;
      color: white !important;
    }
    .swagger-ui .btn.execute:hover {
      background-color: #3fb881 !important;
    }
    .swagger-ui .scheme-container { 
      background: #fafafa; 
      padding: 15px; 
      margin: 20px 0; 
      border-radius: 4px;
    }
    .swagger-ui .opblock.opblock-post .opblock-summary { border-color: #49cc90; }
    .swagger-ui .opblock.opblock-get .opblock-summary { border-color: #61affe; }
  `,
  customSiteTitle: 'DOMjudge Automation API - Interactive Documentation',
  swaggerOptions: {
    // Enable interactive features
    persistAuthorization: false,
    displayRequestDuration: true,
    filter: true,
    tryItOutEnabled: true,
    // Enable all HTTP methods for testing
    supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch', 'head', 'options'],
    // Show models and examples
    defaultModelsExpandDepth: 2,
    defaultModelExpandDepth: 2,
    // Expand operations by default
    docExpansion: 'list',
    // Enable deep linking
    deepLinking: true,
    // Show operation IDs
    displayOperationId: false,
    // Show request/response examples
    showExtensions: true,
    showCommonExtensions: true,
  },
  explorer: true,
};

// Setup Swagger UI - Standard setup that works reliably
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, swaggerUiOptions));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    service: 'domjudge-automation-api',
    message: 'Server is running and ready to accept requests',
  });
});

// Test endpoint for Swagger UI testing
app.get('/api/v1/test', (req, res) => {
  res.json({
    message: 'API is working! You can send requests from Swagger UI.',
    timestamp: new Date().toISOString(),
    method: req.method,
    path: req.path,
  });
});

// Test POST endpoint
app.post('/api/v1/test', (req, res) => {
  res.json({
    message: 'POST request received successfully!',
    timestamp: new Date().toISOString(),
    body: req.body,
    method: req.method,
    path: req.path,
  });
});

// API routes
app.use('/api/v1', teamRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path,
  });
});

// Error handler
app.use(errorHandler);

// Start server
const PORT = config.server.port;

app.listen(PORT, () => {
  logger.info(`Server started on port ${PORT}`, {
    env: config.server.nodeEnv,
    domjudgeApi: config.domjudge.apiBase,
    contestId: config.domjudge.contestId,
  });
  logger.info(`Swagger documentation available at http://localhost:${PORT}/api-docs`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM signal received: closing HTTP server');
  process.exit(0);
});

process.on('SIGINT', () => {
  logger.info('SIGINT signal received: closing HTTP server');
  process.exit(0);
});

export default app;

