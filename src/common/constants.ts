/**
 * Application Constants
 */

export const DATABASE_CONFIG = {
  TYPE: 'sqlite',
  PATH: 'spotify.db',
  SYNCHRONIZE: true,
  LOGGING: false,
};

export enum SubscriptionType {
  FREE = 'FREE',
  PREMIUM = 'PREMIUM',
  STUDENT = 'STUDENT',
}

export const SUBSCRIPTION_PRICES = {
  [SubscriptionType.FREE]: 0.0,
  [SubscriptionType.PREMIUM]: 9.99,
  [SubscriptionType.STUDENT]: 4.99,
};

export const CSV_IMPORT_CONFIG = {
  FILE_PATH: 'spotify_data.csv',
  HEADERS: ['email', 'subType', 'playlistName', 'songTitle', 'artist', 'duration'],
  DELIMITER: ',',
};

export const PAGINATION_CONFIG = {
  DEFAULT_LIMIT: 10,
  DEFAULT_OFFSET: 0,
  MAX_LIMIT: 100,
};
