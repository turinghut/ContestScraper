import express from 'express';
import swaggerUI from 'swagger-ui-express';

// #region local imports
import router from './routes/index';
import swaggerDocument from './config/swagger.config';
import ApiV1Routes from './enumerations/api-routes';
// #endregion

const app = express();

// #region router middlewares
app.use(ApiV1Routes.BaseUrl, router);
app.use(
  ApiV1Routes.SwaggerDocs,
  swaggerUI.serve,
  swaggerUI.setup(swaggerDocument)
);
app.use((_req, res) => {
  res.status(404).send("Sorry can't find that!");
});
// #endregion

export default app;
