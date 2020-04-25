import * as envData from './env-config';
import EnvironmentTypes from '../enumerations/env-types';
import { EnvironmentConfig } from '../interfaces/environment-config';

export const envType: string = process.env.ENV_TYPE || EnvironmentTypes.Development;

export const getEnvObject = (): EnvironmentConfig => {
  switch (envType) {
    case EnvironmentTypes.Development:
      return envData.development;
    case EnvironmentTypes.Production:
      return envData.production;
    default:
      return envData.development;
  }
};
