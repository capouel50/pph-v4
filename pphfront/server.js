const express = require('express');
const path = require('path');

const app = express();

// Middleware de logging pour suivre les requêtes
app.use((req, res, next) => {
  console.log(`Request: ${req.method} ${req.url}`);
  next();
});

// Middleware pour servir les fichiers statiques depuis le dossier 'dist'
app.use(express.static(path.resolve(__dirname, 'dist')));

// Middleware pour gérer toutes les routes et renvoyer 'index.html'
app.get('*', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'dist', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

