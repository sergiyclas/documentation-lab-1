import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

@Entity()
export class Song {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @Column()
  artist: string;

  @Column()
  duration: number;

  @Column({ default: 'Unknown' })
  genre: string;

  @CreateDateColumn()
  createdAt: Date;
}
