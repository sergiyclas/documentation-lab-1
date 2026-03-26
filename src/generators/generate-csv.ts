import * as fs from 'fs';

const generateData = () => {
  const stream = fs.createWriteStream('spotify_data.csv');

  // Headers with genre field
  stream.write('email,subType,playlistName,songTitle,artist,duration,genre\n');

  const subTypes = ['FREE', 'PREMIUM', 'STUDENT'];
  const genres = ['Rock', 'Pop', 'Hip-Hop', 'Jazz', 'Classical', 'Electronic', 'R&B', 'Country'];
  const playlistPrefixes = [
    'Chill',
    'Workout',
    'Party',
    'Study',
    'Night Drive',
    'Focus',
    'Mood',
  ];

  let songsCreated = 0;
  let recordsWritten = 0;

  for (let i = 0; i < 1000; i++) {
    const email = `user${Math.floor(Math.random() * 50)}@example.com`; // 50 unique users
    const subType = subTypes[Math.floor(Math.random() * subTypes.length)];
    const playlistPrefix = playlistPrefixes[Math.floor(Math.random() * playlistPrefixes.length)];
    const playlistNum = Math.floor(Math.random() * 5) + 1;
    const playlistName = `${playlistPrefix}_Playlist_${playlistNum}`;

    // Generate unique song
    const songId = Math.floor(Math.random() * 500) + 1;
    const song = `Track ${songId}`;
    const artistNum = Math.floor(Math.random() * 30) + 1;
    const artist = `Artist ${artistNum}`;
    const duration = 120 + Math.floor(Math.random() * 300); // 2-7 minutes
    const genre = genres[Math.floor(Math.random() * genres.length)];

    stream.write(`${email},${subType},${playlistName},${song},${artist},${duration},${genre}\n`);
    recordsWritten++;
  }

  stream.end();
  console.log(`✅ CSV file generated successfully!`);
  console.log(`📊 Total records written: ${recordsWritten}`);
  console.log(`📁 File: spotify_data.csv`);
};