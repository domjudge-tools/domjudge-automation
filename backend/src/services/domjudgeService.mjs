import axios from 'axios';
import { config } from '../config/index.mjs';
import logger from '../utils/logger.mjs';

export class DomjudgeService {
  constructor() {
    this.contestId = config.domjudge.contestId;

    // Create axios instance with Basic Auth
    this.api = axios.create({
      baseURL: config.domjudge.apiBase,
      auth: {
        username: config.domjudge.username,
        password: config.domjudge.password,
      },
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          logger.error('DOMjudge API Error', {
            status: error.response.status,
            statusText: error.response.statusText,
            data: error.response.data,
            url: error.config?.url,
          });
        } else if (error.request) {
          logger.error('DOMjudge API Request Error', {
            message: error.message,
            url: error.config?.url,
          });
        }
        return Promise.reject(error);
      }
    );
  }

  /**
   * Fetch all existing organizations
   * @returns {Promise<Map<string, string|number>>} Map of organization names to IDs
   */
  async getOrganizations() {
    try {
      const response = await this.api.get(
        `/api/v4/contests/${this.contestId}/organizations`
      );
      const orgMap = new Map();
      response.data.forEach((org) => {
        // Organization ID can be string or number
        orgMap.set(org.name, org.id);
      });
      logger.info(`Fetched ${orgMap.size} organizations`);
      return orgMap;
    } catch (error) {
      logger.error('Failed to fetch organizations', { error });
      throw new Error('Failed to fetch organizations from DOMjudge');
    }
  }

  /**
   * Create a new organization
   * @param {Object} orgData - Organization data
   * @param {string} orgData.id - Organization ID
   * @param {string} orgData.shortname - Short name
   * @param {string} orgData.name - Full name
   * @param {string} orgData.formal_name - Formal name
   * @param {string} orgData.country - Country code
   * @returns {Promise<Object>} Created organization
   */
  async createOrganization(orgData) {
    try {
      const response = await this.api.post(
        `/api/v4/contests/${this.contestId}/organizations`,
        orgData
      );
      logger.info(`Created organization: ${orgData.name}`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 400) {
        logger.warn(`Organization might already exist: ${orgData.name}`);
      }
      throw error;
    }
  }

  /**
   * Fetch all existing teams
   * @returns {Promise<Map<string, number>>} Map of team names to IDs
   */
  async getTeams() {
    try {
      const response = await this.api.get(
        `/api/v4/contests/${this.contestId}/teams`
      );
      const teamMap = new Map();
      response.data.forEach((team) => {
        teamMap.set(team.name, team.id);
      });
      logger.info(`Fetched ${teamMap.size} teams`);
      return teamMap;
    } catch (error) {
      logger.error('Failed to fetch teams', { error });
      throw new Error('Failed to fetch teams from DOMjudge');
    }
  }

  /**
   * Create a new team
   * @param {Object} teamData - Team data
   * @returns {Promise<Object>} Created team
   */
  async createTeam(teamData) {
    try {
      const response = await this.api.post(
        `/api/v4/contests/${this.contestId}/teams`,
        teamData
      );
      logger.info(`Created team: ${teamData.name} with ID ${teamData.id}`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 400) {
        logger.warn(`Team might already exist: ${teamData.name}`);
      }
      throw error;
    }
  }

  /**
   * Fetch all existing users
   * @returns {Promise<Map<string, number>>} Map of usernames to IDs
   */
  async getUsers() {
    try {
      const response = await this.api.get(`/api/v4/users`);
      const userMap = new Map();
      response.data.forEach((user) => {
        userMap.set(user.username, user.id);
      });
      logger.info(`Fetched ${userMap.size} users`);
      return userMap;
    } catch (error) {
      logger.error('Failed to fetch users', { error });
      throw new Error('Failed to fetch users from DOMjudge');
    }
  }

  /**
   * Create a new user
   * @param {Object} userData - User data
   * @returns {Promise<Object>} Created user
   */
  async createUser(userData) {
    try {
      const response = await this.api.post(`/api/v4/users`, userData);
      logger.info(`Created user: ${userData.username} with ID ${userData.id}`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 400) {
        logger.warn(`User might already exist: ${userData.username}`);
      }
      throw error;
    }
  }

  /**
   * Create or get organization
   * @param {string} uniName - University name
   * @param {Map<string, string|number>} existingOrgs - Map of existing organizations
   * @returns {Promise<string|number>} Organization ID
   */
  async createOrGetOrganization(uniName, existingOrgs) {
    if (existingOrgs.has(uniName)) {
      logger.info(`Organization already exists: ${uniName}`);
      return existingOrgs.get(uniName);
    }

    const orgData = {
      id: uniName,
      shortname: uniName,
      name: uniName,
      formal_name: uniName,
      country: 'IRN',
    };

    try {
      const created = await this.createOrganization(orgData);
      // Update the map with the new organization
      // Organization ID is typically the name (string) when created, but API may return differently
      const orgId = created.id || uniName;
      existingOrgs.set(uniName, orgId);
      return orgId;
    } catch (error) {
      // If organization creation fails but it might exist, try to get it
      if (error.response?.status === 400 || error.response?.status === 409) {
        const orgs = await this.getOrganizations();
        if (orgs.has(uniName)) {
          const orgId = orgs.get(uniName);
          existingOrgs.set(uniName, orgId);
          return orgId;
        }
      }
      throw error;
    }
  }
}

export default new DomjudgeService();

