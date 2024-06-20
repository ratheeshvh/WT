const express = require('express');
const mongoose = require('mongoose');
const app = express();
const port = 3000;
app.use(express.json());
mongoose.connect('mongodb://localhost:27017/library', { useNewUrlParser: true, useUnifiedTopology: true });
app.use('/api/books', require('./routes/books'));
app.use('/api/users', require('./routes/users'));
app.use('/api/transactions', require('./routes/transactions'));
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
