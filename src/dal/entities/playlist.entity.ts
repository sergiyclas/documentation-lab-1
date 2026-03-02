import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  ManyToMany,
  JoinTable,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';
import { User } from './user.entity';
import { Song } from './song.entity';

@Entity()
export class Playlist {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column({ nullable: true })
  description: string;

  @ManyToOne(() => User, (user) => user.playlists, { onDelete: 'CASCADE' })
  owner: User;

  @ManyToMany(() => Song, { cascade: true })
  @JoinTable()
  songs: Song[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  /**
   * Get total duration of all songs in playlist (ms)
   */
  getTotalDuration(): number {
    return this.songs.reduce((acc, song) => acc + song.duration, 0);
  }

  /**
   * Get total duration in minutes
   */
  getTotalDurationMinutes(): number {
    return Math.round(this.getTotalDuration() / 60000);
  }
}