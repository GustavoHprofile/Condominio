const http = require('http');
const url = require('url');

// Função para formatar a data no formato DD/MM/YYYY
function formatDateToBrazilian(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
}

// Cria o servidor HTTP
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);

    if (parsedUrl.pathname === '/get-date' && req.method === 'GET') {
        const currentDate = new Date();
        const formattedDate = formatDateToBrazilian(currentDate);

        // Configura o cabeçalho CORS para permitir requisições do frontend
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ date: formattedDate }));
    } else {
        res.statusCode = 404;
        res.end('Not Found');
    }
});

// Define a porta para o servidor
const port = 3000;
server.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});