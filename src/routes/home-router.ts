import express, { Request, Response } from 'express';

const router = express.Router();

router.all('/', (_req: Request, res: Response): void => {
  res.send('You have reached me. Please read the OpenAPI specification for other URLs');
});

export default router;
