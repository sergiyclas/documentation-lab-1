/**
 * View Interface for Business Logic Layer
 * Defines the contract for presentation layer interactions
 */
export interface ISpotifyView {
  renderMenu(): void;
  showStatus(message: string): void;
  showError(error: string): void;
  displayUserInfo(userId: number): void;
  displayPlaylistInfo(playlistId: number): void;
}

/**
 * Statistics View Interface
 * For displaying database statistics
 */
export interface IStatisticsView {
  displayStats(stats: {
    totalUsers: number;
    totalSongs: number;
    totalPlaylists: number;
  }): void;
}