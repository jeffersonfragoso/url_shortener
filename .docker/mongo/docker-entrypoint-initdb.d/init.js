print('Start #################################################################');

db = db.getSiblingDB('dev-shortener');
db.createUser(
  {
    user: 'dev',
    pwd: 'dev123',
    roles: [{ role: 'readWrite', db: 'dev-shortener' }],
  },
);
db.createCollection('urls');

print('END #################################################################');
