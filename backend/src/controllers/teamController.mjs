import domjudgeService from '../services/domjudgeService.mjs';
import {
  generateUniqueId,
  generatePassword,
  generateUsername,
  ensureUniqueUsername,
} from '../utils/idGenerator.mjs';
import logger from '../utils/logger.mjs';

/**
 * Create a single team and user
 * @param {import('express').Request} req - Express request object
 * @param {import('express').Response} res - Express response object
 */
export async function createTeam(req, res) {
  try {
    const teamData = req.body;
    const dryRun = req.query.dryRun === 'true';

    // Validate required fields
    if (!teamData.team || !teamData.uni) {
      res.status(400).json({
        success: false,
        error: 'Team name and university name are required',
      });
      return;
    }

    // Fetch existing data
    const [existingOrgs, existingTeams, existingUsers] = await Promise.all([
      domjudgeService.getOrganizations(),
      domjudgeService.getTeams(),
      domjudgeService.getUsers(),
    ]);

    // Check if team already exists
    if (existingTeams.has(teamData.team)) {
      res.status(409).json({
        success: false,
        error: `Team '${teamData.team}' already exists`,
      });
      return;
    }

    // Prepare ID sets
    const existingIds = new Set([
      ...existingTeams.values(),
      ...existingUsers.values(),
    ]);
    const existingUsernames = new Set(existingUsers.keys());

    // Generate unique ID
    const uniqueId = generateUniqueId(existingIds);

    // Generate or use provided username
    let username = teamData.username;
    if (!username) {
      username = generateUsername(uniqueId);
    }
    username = ensureUniqueUsername(username, existingUsernames);

    // Generate or use provided password
    const password = teamData.password || generatePassword(10);

    if (dryRun) {
      res.json({
        success: true,
        message: 'Dry run - team would be created',
        teamId: uniqueId,
        userId: uniqueId,
        username,
        password,
      });
      return;
    }

    // Create or get organization
    await domjudgeService.createOrGetOrganization(
      teamData.uni,
      existingOrgs
    );

    // Create team
    const teamPayload = {
      id: uniqueId,
      name: teamData.team,
      display_name: teamData.team,
      description: teamData.names || teamData.phone
        ? `${teamData.names || ''} | ${teamData.phone || ''}`.trim()
        : undefined,
      organization_id: teamData.uni,
      group_ids: ['3'],
    };

    const createdTeam = await domjudgeService.createTeam(teamPayload);

    // Create user
    const userPayload = {
      id: uniqueId,
      username,
      name: teamData.team,
      email: teamData.email,
      password,
      enabled: true,
      team_id: uniqueId,
      roles: ['team'],
    };

    const createdUser = await domjudgeService.createUser(userPayload);

    res.status(201).json({
      success: true,
      teamId: createdTeam.id,
      userId: createdUser.id,
      username,
      password,
    });
  } catch (error) {
    logger.error('Error creating team', { error, teamData: req.body });
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to create team',
    });
  }
}

/**
 * Create multiple teams in bulk
 * @param {import('express').Request} req - Express request object
 * @param {import('express').Response} res - Express response object
 */
export async function createTeamsBulk(req, res) {
  try {
    const { teams, dryRun = false } = req.body;

    if (!Array.isArray(teams) || teams.length === 0) {
      res.status(400).json({
        total: 0,
        created: 0,
        skipped: 0,
        failed: 0,
        results: [],
        createdUsers: [],
      });
      return;
    }

    // Fetch existing data once
    const [existingOrgs, existingTeams, existingUsers] = await Promise.all([
      domjudgeService.getOrganizations(),
      domjudgeService.getTeams(),
      domjudgeService.getUsers(),
    ]);

    // Prepare ID sets
    const existingIds = new Set([
      ...existingTeams.values(),
      ...existingUsers.values(),
    ]);
    const existingUsernames = new Set(existingUsers.keys());
    const existingTeamNames = new Set(existingTeams.keys());

    // Filter out teams that already exist
    const teamsToCreate = teams.filter(
      (team) => !existingTeamNames.has(team.team)
    );

    const results = [];
    const createdUsers = [];

    // Process each team
    for (const teamData of teamsToCreate) {
      try {
        // Validate required fields
        if (!teamData.team || !teamData.uni) {
          results.push({
            success: false,
            error: 'Team name and university name are required',
          });
          continue;
        }

        // Generate unique ID
        const uniqueId = generateUniqueId(existingIds);

        // Generate or use provided username
        let username = teamData.username;
        if (!username) {
          username = generateUsername(uniqueId);
        }
        username = ensureUniqueUsername(username, existingUsernames);

        // Generate or use provided password
        const password = teamData.password || generatePassword(10);

        if (dryRun) {
          results.push({
            success: true,
            message: 'Dry run - team would be created',
            teamId: uniqueId,
            userId: uniqueId,
            username,
            password,
          });
          createdUsers.push({
            team: teamData.team,
            id: uniqueId,
            username,
            names: teamData.names,
            email: teamData.email,
            phone: teamData.phone,
            password,
          });
          continue;
        }

        // Create or get organization
        await domjudgeService.createOrGetOrganization(
          teamData.uni,
          existingOrgs
        );

        // Create team
        const teamPayload = {
          id: uniqueId,
          name: teamData.team,
          display_name: teamData.team,
          description: teamData.names || teamData.phone
            ? `${teamData.names || ''} | ${teamData.phone || ''}`.trim()
            : undefined,
          organization_id: teamData.uni,
          group_ids: ['3'],
        };

        const createdTeam = await domjudgeService.createTeam(teamPayload);

        // Create user
        const userPayload = {
          id: uniqueId,
          username,
          name: teamData.team,
          email: teamData.email,
          password,
          enabled: true,
          team_id: uniqueId,
          roles: ['team'],
        };

        const createdUser = await domjudgeService.createUser(userPayload);

        results.push({
          success: true,
          teamId: createdTeam.id,
          userId: createdUser.id,
          username,
          password,
        });

        createdUsers.push({
          team: teamData.team,
          id: createdUser.id,
          username,
          names: teamData.names,
          email: teamData.email,
          phone: teamData.phone,
          password,
        });
      } catch (error) {
        logger.error('Error creating team in bulk', {
          error,
          teamData,
        });
        results.push({
          success: false,
          error: error.message || 'Failed to create team',
        });
      }
    }

    // Calculate statistics
    const created = results.filter((r) => r.success).length;
    const failed = results.filter((r) => !r.success).length;
    const skipped = teams.length - teamsToCreate.length;

    res.status(201).json({
      total: teams.length,
      created,
      skipped,
      failed,
      results,
      createdUsers,
    });
  } catch (error) {
    logger.error('Error in bulk team creation', { error });
    res.status(500).json({
      total: req.body.teams?.length || 0,
      created: 0,
      skipped: 0,
      failed: req.body.teams?.length || 0,
      results: [],
      createdUsers: [],
    });
  }
}

/**
 * Get all teams
 * @param {import('express').Request} req - Express request object
 * @param {import('express').Response} res - Express response object
 */
export async function getTeams(req, res) {
  try {
    const teams = await domjudgeService.getTeams();
    const teamsArray = Array.from(teams.entries()).map(([name, id]) => ({
      name,
      id,
    }));
    res.json(teamsArray);
  } catch (error) {
    logger.error('Error fetching teams', { error });
    res.status(500).json({
      error: error.message || 'Failed to fetch teams',
    });
  }
}

/**
 * Get all organizations
 * @param {import('express').Request} req - Express request object
 * @param {import('express').Response} res - Express response object
 */
export async function getOrganizations(req, res) {
  try {
    const orgs = await domjudgeService.getOrganizations();
    const orgsArray = Array.from(orgs.entries()).map(([name, id]) => ({
      name,
      id,
    }));
    res.json(orgsArray);
  } catch (error) {
    logger.error('Error fetching organizations', { error });
    res.status(500).json({
      error: error.message || 'Failed to fetch organizations',
    });
  }
}

/**
 * Get all users
 * @param {import('express').Request} req - Express request object
 * @param {import('express').Response} res - Express response object
 */
export async function getUsers(req, res) {
  try {
    const users = await domjudgeService.getUsers();
    const usersArray = Array.from(users.entries()).map(([username, id]) => ({
      username,
      id,
    }));
    res.json(usersArray);
  } catch (error) {
    logger.error('Error fetching users', { error });
    res.status(500).json({
      error: error.message || 'Failed to fetch users',
    });
  }
}

