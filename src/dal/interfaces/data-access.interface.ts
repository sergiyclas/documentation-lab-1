import { User } from '../entities/user.entity';
import { Song } from '../entities/song.entity';
import { Playlist } from '../entities/playlist.entity';

export interface IDataAccessLayer {
  findUserByEmail(email: string): Promise<User | null>;
  findUserById(id: number): Promise<User | null>;
  saveUser(user: User): Promise<User>;
  getAllUsers(): Promise<User[]>;
  deleteUser(id: number): Promise<void>;

  findSong(title: string, artist: string): Promise<Song | null>;
  findSongById(id: number): Promise<Song | null>;
  saveSong(song: Song): Promise<Song>;
  getAllSongs(): Promise<Song[]>;

  findPlaylistById(id: number): Promise<Playlist | null>;
  getPlaylistsByUser(userId: number): Promise<Playlist[]>;
  savePlaylist(playlist: Playlist): Promise<Playlist>;
  deletePlaylist(id: number): Promise<void>;

  getTotalUsers(): Promise<number>;
  getTotalSongs(): Promise<number>;
  getTotalPlaylists(): Promise<number>;
}

// Token для ін'єкції (NestJS специфіка)
export const DATA_ACCESS_LAYER = 'IDataAccessLayer';