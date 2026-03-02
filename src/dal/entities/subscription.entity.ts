import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  TableInheritance,
  OneToOne,
  ChildEntity,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';
import { User } from './user.entity';

@Entity()
@TableInheritance({ column: { type: 'varchar', name: 'type' } })
export abstract class Subscription {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ default: true })
  autoRenew: boolean;

  @OneToOne(() => User, (user) => user.subscription)
  user: User;

  @CreateDateColumn()
  startDate: Date;

  @Column({ nullable: true })
  endDate: Date;

  abstract getPrice(): number;
  abstract getType(): string;

  /**
   * Check if subscription is active
   */
  isActive(): boolean {
    const now = new Date();
    return !this.endDate || this.endDate > now;
  }

  /**
   * Get remaining days of subscription
   */
  getRemainingDays(): number {
    if (!this.endDate) return -1; // Unlimited
    const now = new Date();
    if (this.endDate <= now) return 0;
    return Math.ceil((this.endDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
  }
}

@ChildEntity()
export class FreeSubscription extends Subscription {
  getPrice() {
    return 0.0;
  }

  getType() {
    return 'FREE';
  }
}

@ChildEntity()
export class PremiumSubscription extends Subscription {
  @Column({ default: false })
  hasOfflineDownload: boolean;

  @Column({ default: true })
  hasHighQuality: boolean;

  getPrice() {
    return 9.99;
  }

  getType() {
    return 'PREMIUM';
  }
}

@ChildEntity()
export class StudentSubscription extends Subscription {
  @Column({ nullable: true })
  university: string;

  @Column({ nullable: true })
  studentId: string;

  getPrice() {
    return 4.99;
  }

  getType() {
    return 'STUDENT';
  }
}