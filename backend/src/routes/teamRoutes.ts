import { Router } from 'express';
import { body, query } from 'express-validator';
import {
  createTeam,
  createTeamsBulk,
  getTeams,
  getOrganizations,
  getUsers,
} from '../controllers/teamController';
import { validateRequest } from '../middleware/validation';

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

// Routes
router.post(
  '/teams',
  createTeamValidation,
  validateRequest,
  createTeam
);

router.post(
  '/teams/bulk',
  createTeamsBulkValidation,
  validateRequest,
  createTeamsBulk
);

router.get('/teams', getTeams);

router.get('/organizations', getOrganizations);

router.get('/users', getUsers);

export default router;

