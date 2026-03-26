import { Inject, Injectable } from '@nestjs/common';
import * as fs from 'fs';
import * as readline from 'readline';
import { DATA_ACCESS_LAYER, IDataAccessLayer } from '../../dal/interfaces/data-access.interface';
import { User } from '../../dal/entities/user.entity';
import { Song } from '../../dal/entities/song.entity';
import { Playlist } from '../../dal/entities/playlist.entity';
import {
  FreeSubscription,
  PremiumSubscription,
  StudentSubscription,
} from '../../dal/entities/subscription.entity';
import { Logger } from '../../common/logger';

@Injectable()
export class SpotifyService {
  private readonly logger = new Logger('SpotifyService');

  constructor(
    @Inject(DATA_ACCESS_LAYER) private readonly dal: IDataAccessLayer,
  ) {}

  async importData(filePath: string): Promise<void> {
    try {
      this.logger.info(`🚀 Starting data import from ${filePath}`);

      const fileStream = fs.createReadStream(filePath);
      const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

      let lineCount = 0;
      let isHeader = true;
      const stats = { usersCreated: 0, songsCreated: 0, playlistsCreated: 0 };

      for await (const line of rl) {
        lineCount++;

        if (isHeader) {
          isHeader = false;
          this.logger.debug(`CSV Headers: ${line}`);
          continue;
        }

        const [email, subType, playlistName, songTitle, artist, durationStr, genre] = line.split(
          ',',
        );
        const duration = parseInt(durationStr, 10);

        try {
          let song = await this.dal.findSong(songTitle, artist);
          if (!song) {
            song = new Song();
            song.title = songTitle;
            song.artist = artist;
            song.duration = duration;
            song.genre = genre || 'Unknown';
            song = await this.dal.saveSong(song);
            stats.songsCreated++;
            this.logger.debug(`✅ Song created: ${songTitle} by ${artist}`);
          }

          let user = await this.dal.findUserByEmail(email);
          if (!user) {
            user = new User();
            user.email = email;
            user.username = email.split('@')[0];
            user.playlists = [];

            switch (subType.toUpperCase()) {
              case 'PREMIUM':
                user.subscription = new PremiumSubscription();
                break;
              case 'STUDENT':
                user.subscription = new StudentSubscription();
                break;
              default:
                user.subscription = new FreeSubscription();
            }

            stats.usersCreated++;
            this.logger.debug(`✅ User created: ${email} (${subType})`);
          }

          let playlist = user.playlists.find((p) => p.name === playlistName);
          if (!playlist) {
            playlist = new Playlist();
            playlist.name = playlistName;
            playlist.description = `Auto-generated playlist: ${playlistName}`;
            playlist.songs = [];
            user.playlists.push(playlist);
            stats.playlistsCreated++;
            this.logger.debug(`✅ Playlist created: ${playlistName}`);
          }

          const songExistsInPlaylist = playlist.songs.some((s) => s.id === song.id);
          if (!songExistsInPlaylist) {
            playlist.songs.push(song);
          }

          await this.dal.saveUser(user);

          if (lineCount % 100 === 0) {
            this.logger.info(`📊 Processed ${lineCount} lines...`);
          }
        } catch (error) {
          this.logger.error(`Error processing line ${lineCount}: ${line}`, error as Error);
        }
      }

      this.logger.info('✅ Import completed!', {
        totalLines: lineCount - 1,
        usersCreated: stats.usersCreated,
        songsCreated: stats.songsCreated,
        playlistsCreated: stats.playlistsCreated,
      });
    } catch (error) {
      this.logger.error('Critical error during import', error as Error);
      throw error;
    }
  }
}