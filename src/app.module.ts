import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { SpotifyService } from './bll/services/spotify.service';
import { DataAccessService } from './dal/repositories/data-access.service';
import { DATA_ACCESS_LAYER } from './dal/interfaces/data-access.interface';
import { User } from './dal/entities/user.entity';
import { Song } from './dal/entities/song.entity';
import { Playlist } from './dal/entities/playlist.entity';
import {
  Subscription,
  FreeSubscription,
  PremiumSubscription,
  StudentSubscription,
} from './dal/entities/subscription.entity';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'sqlite',
      database: 'spotify.db',
      entities: [
        User,
        Song,
        Playlist,
        Subscription,
        FreeSubscription,
        PremiumSubscription,
        StudentSubscription,
      ],
      synchronize: true, // Auto-create/update tables in development
      logging: false,
    }),
    TypeOrmModule.forFeature([User, Song, Playlist, Subscription]),
  ],
  providers: [
    SpotifyService,
    DataAccessService,
    {
      provide: DATA_ACCESS_LAYER,
      useClass: DataAccessService,
    },
  ],
})
export class AppModule {}