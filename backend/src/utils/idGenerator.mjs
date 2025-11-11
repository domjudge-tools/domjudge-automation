/**
 * Generates a unique numeric ID within a specified range
 * @param {Set<number>} existingIds - Set of existing IDs to avoid duplicates
 * @param {number} lower - Lower bound for ID generation (default: 10000)
 * @param {number} upper - Upper bound for ID generation (default: 99999)
 * @returns {number} Unique numeric ID
 */
export function generateUniqueId(
  existingIds,
  lower = 10000,
  upper = 99999
) {
  const maxAttempts = 10000;
  let attempts = 0;

  while (attempts < maxAttempts) {
    const newId = Math.floor(Math.random() * (upper - lower + 1)) + lower;
    if (!existingIds.has(newId)) {
      existingIds.add(newId);
      return newId;
    }
    attempts++;
  }

  throw new Error(
    `Failed to generate unique ID after ${maxAttempts} attempts. Range: ${lower}-${upper}`
  );
}

/**
 * Generates a random alphanumeric password
 * @param {number} length - Password length (default: 10)
 * @returns {string} Random password
 */
export function generatePassword(length = 10) {
  const chars =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let password = '';
  for (let i = 0; i < length; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return password;
}

/**
 * Generates a username from a numeric ID
 * @param {number} id - Numeric ID
 * @param {string} prefix - Username prefix (default: 'T')
 * @returns {string} Generated username
 */
export function generateUsername(id, prefix = 'T') {
  return `${prefix}${id}`;
}

/**
 * Ensures username uniqueness by appending a suffix if needed
 * @param {string} baseUsername - Base username
 * @param {Set<string>} existingUsernames - Set of existing usernames
 * @param {number} [suffix] - Optional suffix to start with
 * @returns {string} Unique username
 */
export function ensureUniqueUsername(
  baseUsername,
  existingUsernames,
  suffix
) {
  if (!existingUsernames.has(baseUsername)) {
    existingUsernames.add(baseUsername);
    return baseUsername;
  }

  // Try with suffix
  const suffixToUse = suffix || 1;
  const newUsername = `${baseUsername}${suffixToUse}`;

  if (!existingUsernames.has(newUsername)) {
    existingUsernames.add(newUsername);
    return newUsername;
  }

  // Recursive call with incremented suffix
  return ensureUniqueUsername(baseUsername, existingUsernames, suffixToUse + 1);
}

