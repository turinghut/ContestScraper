import { getEnvObject } from './config/env-helper';
import expressApp from './app';
import init from './signals';

const envObject = getEnvObject();

const server = expressApp.listen(envObject.port, () => {
  console.log(`Server started on ${envObject.port} port`);
});

const shutdown = init(() => {
  server.close(async () => {
    // clean any thing related to database or something else
    console.log('Shutting down the server');
  });
});

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
