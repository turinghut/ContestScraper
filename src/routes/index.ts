import express from 'express'
import homeRouter from './home-router'

const router = express.Router()

router.use('/', homeRouter)

router.use((req, res, next) => {
  res.status(404).send("Sorry can't find that!")
})

export default router
