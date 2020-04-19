import { EnvironmentConfig } from '../interfaces/environment-config';

export const development: EnvironmentConfig = {
  host: '127.0.0.1',
  port: 3000,
};

export const production: EnvironmentConfig = {
  host: '127.0.0.1',
  port: 80,
};
