import ApiV1Routes from '../enumerations/api-routes';
import { getEnvObject } from './env-helper';

const envObject = getEnvObject();

const swaggerDocument = {
  swagger: '2.0',
  info: {
    description:
      'This API is used to retrieve the contest details from CodeChef, Codeforces and many other websites',
    version: '1.0.0',
    title: 'Contest Scraper',
    contact: { email: 'turinghut@vnrvjiet.in' },
    license: {
      name: 'Apache 2.0',
      url: 'http://www.apache.org/licenses/LICENSE-2.0.html',
    },
  },
  host: `${envObject.host}:${envObject.port}`,
  basePath: ApiV1Routes.BaseUrl,
  tags: [],
  schemes: ['http'],
  // Paths are definitions of swagger go here. Take a look at https://petstore.swagger.io/v2/swagger.json
  paths: {},
  definitions: {},
  externalDocs: {
    description: 'Find out more about Swagger',
    url: 'http://swagger.io',
  },
};

export default swaggerDocument;
