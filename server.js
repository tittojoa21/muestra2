const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 3000;

const upload = multer({ dest: 'uploads/' });

app.use('/images', express.static(path.join(__dirname, 'uploads')));

app.post('/upload', upload.array('images'), (req, res) => {
    res.json({ message: 'Imágenes cargadas exitosamente' });
});

app.get('/images', (req, res) => {
    fs.readdir(path.join(__dirname, 'uploads'), (err, files) => {
        if (err) {
            res.status(500).json({ error: 'Error al obtener las imágenes' });
        } else {
            res.json(files);
        }
    });
});

app.listen(port, () => {
    console.log(`Servidor escuchando en http://localhost:${port}`);
});
