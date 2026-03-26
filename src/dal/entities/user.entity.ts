import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  OneToMany,
  OneToOne,
  JoinColumn,
  CreateDateColumn,
  UpdateDateColumn,
  Index,
} from 'typeorm';
import { Playlist } from './playlist.entity';
import { Subscription } from './subscription.entity';

@Entity()
@Index(['email'], { unique: true })
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  email: string;

  @Column({ nullable: true })
  username: string;

  @OneToOne(() => Subscription, (sub) => sub.user, { cascade: true, eager: true })
  @JoinColumn()
  subscription: Subscription;

  @OneToMany(() => Playlist, (playlist) => playlist.owner, { cascade: true, eager: true })
  playlists: Playlist[];

  @CreateDateColumn()
  registrationDate: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @Column({ default: true })
  isActive: boolean;

  getTotalSongs(): number {
    return this.playlists.reduce((acc, playlist) => acc + playlist.songs.length, 0);
  }

  getUniqueSongs() {
    const songMap = new Map();
    this.playlists.forEach((playlist) => {
      playlist.songs.forEach((song) => {
        if (!songMap.has(song.id)) {
          songMap.set(song.id, song);
        }
      });
    });
    return Array.from(songMap.values());
  }
}