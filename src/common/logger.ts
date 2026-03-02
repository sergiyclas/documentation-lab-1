/**
 * Logger Service
 * Простий логер для додатку
 */

export enum LogLevel {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR',
}

export class Logger {
  private context: string;
  private logLevel: LogLevel = LogLevel.DEBUG;

  constructor(context: string) {
    this.context = context;
  }

  debug(message: string, meta?: any) {
    if (this.logLevel === LogLevel.DEBUG) {
      console.log(`[${this.context}] 🔵 ${message}`, meta || '');
    }
  }

  info(message: string, meta?: any) {
    console.log(`[${this.context}] ℹ️ ${message}`, meta || '');
  }

  warn(message: string, meta?: any) {
    console.warn(`[${this.context}] ⚠️ ${message}`, meta || '');
  }

  error(message: string, error?: Error) {
    console.error(`[${this.context}] ❌ ${message}`, error || '');
  }
}
