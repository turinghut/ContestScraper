import express from 'express';
import ApiV1Routes from '../enumerations/api-routes';
import homeRouter from './home-router';

const router = express.Router();

router.route(ApiV1Routes.Home).all(homeRouter);

export default router;
