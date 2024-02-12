// redisClient.js
const Redis = require("ioredis");
const redis = new Redis(process.env.MEMETRIA_REDIS_URL);

module.exports = redis;
