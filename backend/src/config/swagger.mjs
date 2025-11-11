import swaggerJsdoc from 'swagger-jsdoc';
import { config } from './index.mjs';

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'DOMjudge Automation API',
      version: '1.0.0',
      description: 'API for automating team and user creation in DOMjudge contest management system',
      contact: {
        name: 'API Support',
      },
    },
    servers: [
      {
        url: `http://localhost:${config.server.port}`,
        description: 'Development server',
      },
    ],
    components: {
      schemas: {
        CreateTeamRequest: {
          type: 'object',
          required: ['team', 'uni'],
          properties: {
            team: {
              type: 'string',
              description: 'Team name',
              example: 'Team Alpha',
            },
            uni: {
              type: 'string',
              description: 'University/Organization name',
              example: 'University of Technology',
            },
            username: {
              type: 'string',
              description: 'Username (optional, auto-generated if not provided)',
              example: 'T12345',
            },
            password: {
              type: 'string',
              description: 'Password (optional, auto-generated if not provided)',
              example: 'password123',
            },
            email: {
              type: 'string',
              format: 'email',
              description: 'Email address (optional)',
              example: 'team@example.com',
            },
            names: {
              type: 'string',
              description: 'Team member names (optional)',
              example: 'Member1, Member2, Member3',
            },
            phone: {
              type: 'string',
              description: 'Phone number (optional)',
              example: '1234567890',
            },
          },
        },
        CreateTeamResponse: {
          type: 'object',
          properties: {
            success: {
              type: 'boolean',
              example: true,
            },
            teamId: {
              type: 'number',
              example: 12345,
            },
            userId: {
              type: 'number',
              example: 12345,
            },
            username: {
              type: 'string',
              example: 'T12345',
            },
            password: {
              type: 'string',
              example: 'abc123xyz',
            },
            message: {
              type: 'string',
              example: 'Dry run - team would be created',
            },
            error: {
              type: 'string',
              example: 'Error message',
            },
          },
        },
        CreateTeamsBulkRequest: {
          type: 'object',
          required: ['teams'],
          properties: {
            teams: {
              type: 'array',
              items: {
                $ref: '#/components/schemas/CreateTeamRequest',
              },
            },
            dryRun: {
              type: 'boolean',
              description: 'If true, simulate creation without actually creating',
              example: false,
            },
          },
        },
        CreateTeamsBulkResponse: {
          type: 'object',
          properties: {
            total: {
              type: 'number',
              example: 10,
            },
            created: {
              type: 'number',
              example: 8,
            },
            skipped: {
              type: 'number',
              example: 1,
            },
            failed: {
              type: 'number',
              example: 1,
            },
            results: {
              type: 'array',
              items: {
                $ref: '#/components/schemas/CreateTeamResponse',
              },
            },
            createdUsers: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  team: {
                    type: 'string',
                    example: 'Team Alpha',
                  },
                  id: {
                    type: 'number',
                    example: 12345,
                  },
                  username: {
                    type: 'string',
                    example: 'T12345',
                  },
                  names: {
                    type: 'string',
                    example: 'Member1, Member2',
                  },
                  email: {
                    type: 'string',
                    example: 'team@example.com',
                  },
                  phone: {
                    type: 'string',
                    example: '1234567890',
                  },
                  password: {
                    type: 'string',
                    example: 'abc123xyz',
                  },
                },
              },
            },
          },
        },
        Team: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              example: 'Team Alpha',
            },
            id: {
              type: 'number',
              example: 12345,
            },
          },
        },
        Organization: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              example: 'University of Technology',
            },
            id: {
              oneOf: [
                { type: 'string' },
                { type: 'number' },
              ],
              example: 'University of Technology',
            },
          },
        },
        User: {
          type: 'object',
          properties: {
            username: {
              type: 'string',
              example: 'T12345',
            },
            id: {
              type: 'number',
              example: 12345,
            },
          },
        },
        Error: {
          type: 'object',
          properties: {
            error: {
              type: 'string',
              example: 'Error message',
            },
            errors: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  msg: {
                    type: 'string',
                  },
                  param: {
                    type: 'string',
                  },
                  location: {
                    type: 'string',
                  },
                },
              },
            },
          },
        },
        HealthCheck: {
          type: 'object',
          properties: {
            status: {
              type: 'string',
              example: 'ok',
            },
            timestamp: {
              type: 'string',
              format: 'date-time',
            },
            service: {
              type: 'string',
              example: 'domjudge-automation-api',
            },
          },
        },
      },
    },
    tags: [
      {
        name: 'Teams',
        description: 'Team management endpoints',
      },
      {
        name: 'Organizations',
        description: 'Organization management endpoints',
      },
      {
        name: 'Users',
        description: 'User management endpoints',
      },
      {
        name: 'Health',
        description: 'Health check endpoints',
      },
    ],
  },
  apis: ['./src/**/*.mjs'],
};

export const swaggerSpec = swaggerJsdoc(options);

