import { Request, Response } from 'express';
// eslint-disable-next-line import/no-unresolved
import { ParamsDictionary, Query } from 'express-serve-static-core';

const homeRoute = (
  _req: Request<ParamsDictionary, unknown, unknown, Query>,
  res: Response<unknown>
): void => {
  res.send(
    'You have reached me. Please read the OpenAPI specification for other URLs'
  );
};

export default homeRoute;
