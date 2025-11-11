export interface TeamData {
  team: string;
  username?: string;
  password?: string;
  uni: string;
  email?: string;
  names?: string;
  phone?: string;
}

export interface Organization {
  id: string | number;
  shortname: string;
  name: string;
  formal_name: string;
  country: string;
}

export interface Team {
  id: number;
  name: string;
  display_name: string;
  description?: string;
  organization_id: string | number;
  group_ids: string[];
}

export interface User {
  id: number;
  username: string;
  name: string;
  email?: string;
  password: string;
  enabled: boolean;
  team_id: number;
  roles: string[];
}

export interface CreatedUser {
  team: string;
  id: number;
  username: string;
  names?: string;
  email?: string;
  phone?: string;
  password: string;
}

export interface CreateTeamRequest {
  team: string;
  username?: string;
  password?: string;
  uni: string;
  email?: string;
  names?: string;
  phone?: string;
}

export interface CreateTeamsBulkRequest {
  teams: CreateTeamRequest[];
  dryRun?: boolean;
}

export interface CreateTeamResponse {
  success: boolean;
  teamId?: number;
  userId?: number;
  username?: string;
  password?: string;
  message?: string;
  error?: string;
}

export interface CreateTeamsBulkResponse {
  total: number;
  created: number;
  skipped: number;
  failed: number;
  results: CreateTeamResponse[];
  createdUsers: CreatedUser[];
}

