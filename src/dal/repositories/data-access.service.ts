import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { IDataAccessLayer } from '../interfaces/data-access.interface';
import { User } from '../entities/user.entity';
import { Song } from '../entities/song.entity';
import { Playlist } from '../entities/playlist.entity';

@Injectable()
export class DataAccessService implements IDataAccessLayer {
  constructor(
    @InjectRepository(User) private readonly userRepo: Repository<User>,
    @InjectRepository(Song) private readonly songRepo: Repository<Song>,
    @InjectRepository(Playlist) private readonly playlistRepo: Repository<Playlist>,
  ) {}

  /**
   * User Operations
   */
  async findUserByEmail(email: string): Promise<User | null> {
    return this.userRepo.findOne({
      where: { email },
      relations: ['playlists', 'playlists.songs', 'subscription'],
    });
  }

  async findUserById(id: number): Promise<User | null> {
    return this.userRepo.findOne({
      where: { id },
      relations: ['playlists', 'playlists.songs', 'subscription'],
    });
  }

  async saveUser(user: User): Promise<User> {
    return this.userRepo.save(user);
  }

  async getAllUsers(): Promise<User[]> {
    return this.userRepo.find({
      relations: ['playlists', 'playlists.songs', 'subscription'],
    });
  }

  async deleteUser(id: number): Promise<void> {
    await this.userRepo.delete(id);
  }

  /**
   * Song Operations
   */
  async findSong(title: string, artist: string): Promise<Song | null> {
    return this.songRepo.findOne({ where: { title, artist } });
  }

  async findSongById(id: number): Promise<Song | null> {
    return this.songRepo.findOne({ where: { id } });
  }

  async saveSong(song: Song): Promise<Song> {
    return this.songRepo.save(song);
  }

  async getAllSongs(): Promise<Song[]> {
    return this.songRepo.find();
  }

  /**
   * Playlist Operations
   */
  async findPlaylistById(id: number): Promise<Playlist | null> {
    return this.playlistRepo.findOne({
      where: { id },
      relations: ['songs', 'owner'],
    });
  }

  async getPlaylistsByUser(userId: number): Promise<Playlist[]> {
    return this.playlistRepo.find({
      where: { owner: { id: userId } },
      relations: ['songs'],
    });
  }

  async savePlaylist(playlist: Playlist): Promise<Playlist> {
    return this.playlistRepo.save(playlist);
  }

  async deletePlaylist(id: number): Promise<void> {
    await this.playlistRepo.delete(id);
  }

  /**
   * Statistics
   */
  async getTotalUsers(): Promise<number> {
    return this.userRepo.count();
  }

  async getTotalSongs(): Promise<number> {
    return this.songRepo.count();
  }

  async getTotalPlaylists(): Promise<number> {
    return this.playlistRepo.count();
  }
}