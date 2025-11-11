import { Router } from 'express';
import { body } from 'express-validator';
import {
  createTeam,
  createTeamsBulk,
  getTeams,
  getOrganizations,
  getUsers,
} from '../controllers/teamController.mjs';
import { validateRequest } from '../middleware/validation.mjs';

const router = Router();

// Validation rules
const createTeamValidation = [
  body('team').notEmpty().withMessage('Team name is required'),
  body('uni').notEmpty().withMessage('University name is required'),
  body('username').optional().isString(),
  body('password').optional().isString(),
  body('email').optional().isEmail().withMessage('Invalid email format'),
  body('names').optional().isString(),
  body('phone').optional().isString(),
];

const createTeamsBulkValidation = [
  body('teams')
    .isArray()
    .withMessage('Teams must be an array')
    .notEmpty()
    .withMessage('Teams array cannot be empty'),
  body('teams.*.team')
    .notEmpty()
    .withMessage('Team name is required for all teams'),
  body('teams.*.uni')
    .notEmpty()
    .withMessage('University name is required for all teams'),
  body('teams.*.username').optional().isString(),
  body('teams.*.password').optional().isString(),
  body('teams.*.email').optional().isEmail().withMessage('Invalid email format'),
  body('teams.*.names').optional().isString(),
  body('teams.*.phone').optional().isString(),
  body('dryRun').optional().isBoolean(),
];

/**
 * @swagger
 * /api/v1/teams:
 *   post:
 *     summary: Create a single team and user
 *     description: Creates a new team and associated user account in DOMjudge. Auto-generates username and password if not provided.
 *     tags: [Teams]
 *     parameters:
 *       - in: query
 *         name: dryRun
 *         schema:
 *           type: boolean
 *           default: false
 *         description: If true, simulate creation without actually creating
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/CreateTeamRequest'
 *           examples:
 *             example1:
 *               summary: Basic team creation
 *               value:
 *                 team: "Team Alpha"
 *                 uni: "University of Technology"
 *             example2:
 *               summary: Team with all fields
 *               value:
 *                 team: "Team Beta"
 *                 uni: "University of Science"
 *                 username: "T12345"
 *                 password: "securepass123"
 *                 email: "teambeta@example.com"
 *                 names: "John Doe, Jane Smith"
 *                 phone: "1234567890"
 *     responses:
 *       201:
 *         description: Team and user created successfully
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/CreateTeamResponse'
 *             example:
 *               success: true
 *               teamId: 12345
 *               userId: 12345
 *               username: "T12345"
 *               password: "abc123xyz"
 *       400:
 *         description: Bad request - validation error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 *       409:
 *         description: Team already exists
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/CreateTeamResponse'
 *       500:
 *         description: Internal server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 */
router.post(
  '/teams',
  createTeamValidation,
  validateRequest,
  createTeam
);

/**
 * @swagger
 * /api/v1/teams/bulk:
 *   post:
 *     summary: Create multiple teams and users in bulk
 *     description: Creates multiple teams and associated user accounts in DOMjudge. Automatically skips teams that already exist.
 *     tags: [Teams]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/CreateTeamsBulkRequest'
 *           examples:
 *             example1:
 *               summary: Bulk create teams
 *               value:
 *                 dryRun: false
 *                 teams:
 *                   - team: "Team Alpha"
 *                     uni: "University A"
 *                   - team: "Team Beta"
 *                     uni: "University B"
 *                     email: "teambeta@example.com"
 *             example2:
 *               summary: Dry run mode
 *               value:
 *                 dryRun: true
 *                 teams:
 *                   - team: "Team Gamma"
 *                     uni: "University C"
 *     responses:
 *       201:
 *         description: Teams and users created successfully
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/CreateTeamsBulkResponse'
 *             example:
 *               total: 2
 *               created: 2
 *               skipped: 0
 *               failed: 0
 *               results:
 *                 - success: true
 *                   teamId: 12345
 *                   userId: 12345
 *                   username: "T12345"
 *                   password: "abc123xyz"
 *               createdUsers:
 *                 - team: "Team Alpha"
 *                   id: 12345
 *                   username: "T12345"
 *                   password: "abc123xyz"
 *       400:
 *         description: Bad request - validation error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 *       500:
 *         description: Internal server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 */
router.post(
  '/teams/bulk',
  createTeamsBulkValidation,
  validateRequest,
  createTeamsBulk
);

/**
 * @swagger
 * /api/v1/teams:
 *   get:
 *     summary: Get all teams
 *     tags: [Teams]
 *     responses:
 *       200:
 *         description: List of all teams
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Team'
 *       500:
 *         description: Internal server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 */
router.get('/teams', getTeams);

/**
 * @swagger
 * /api/v1/organizations:
 *   get:
 *     summary: Get all organizations
 *     tags: [Organizations]
 *     responses:
 *       200:
 *         description: List of all organizations
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Organization'
 *       500:
 *         description: Internal server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 */
router.get('/organizations', getOrganizations);

/**
 * @swagger
 * /api/v1/users:
 *   get:
 *     summary: Get all users
 *     tags: [Users]
 *     responses:
 *       200:
 *         description: List of all users
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/User'
 *       500:
 *         description: Internal server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 */
router.get('/users', getUsers);

export default router;
