/**
 * Generates a unique numeric ID within a specified range
 */
export function generateUniqueId(
  existingIds: Set<number>,
  lower: number = 10000,
  upper: number = 99999
): number {
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
 */
export function generatePassword(length: number = 10): string {
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
 */
export function generateUsername(id: number, prefix: string = 'T'): string {
  return `${prefix}${id}`;
}

/**
 * Ensures username uniqueness by appending a suffix if needed
 */
export function ensureUniqueUsername(
  baseUsername: string,
  existingUsernames: Set<string>,
  suffix?: number
): string {
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

