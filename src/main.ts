import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { SpotifyService } from './bll/services/spotify.service';
import { DataAccessService } from './dal/repositories/data-access.service';
import { Logger } from './common/logger';

async function bootstrap() {
  const logger = new Logger('Bootstrap');

  try {
    logger.info('🚀 Starting Spotify Documentation Lab Application...');
    const app = await NestFactory.createApplicationContext(AppModule);

    const spotifyService = app.get(SpotifyService);
    const dataAccessService = app.get(DataAccessService);

    // Import data from CSV
    logger.info('📥 Beginning data import process...');
    await spotifyService.importData('spotify_data.csv');

    // Display statistics
    setTimeout(async () => {
      try {
        const totalUsers = await dataAccessService.getTotalUsers();
        const totalSongs = await dataAccessService.getTotalSongs();
        const totalPlaylists = await dataAccessService.getTotalPlaylists();

        logger.info('\n');
        logger.info('═══════════════════════════════════════════════');
        logger.info('📊 DATABASE STATISTICS');
        logger.info('═══════════════════════════════════════════════');
        logger.info(`✅ Total Users: ${totalUsers}`);
        logger.info(`✅ Total Songs: ${totalSongs}`);
        logger.info(`✅ Total Playlists: ${totalPlaylists}`);
        logger.info('═══════════════════════════════════════════════');
        logger.info(`📁 Database: spotify.db`);
        logger.info(`📄 CSV File: spotify_data.csv`);
        logger.info(`⏰ Import completed successfully!\n`);

        await app.close();
        process.exit(0);
      } catch (error) {
        logger.error('Error retrieving statistics', error as Error);
        await app.close();
        process.exit(1);
      }
    }, 500);
  } catch (error) {
    logger.error('Fatal error during bootstrapping', error as Error);
    process.exit(1);
  }
}

bootstrap();