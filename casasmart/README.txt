CASASMART - INTERFACE WEB

1) Crie o banco: abra o MySQL e rode o arquivo banco.sql
   (ele cria o banco casasmart, as tabelas e os dados de exemplo)

2) Instale as bibliotecas:
   pip install -r requirements.txt

3) Abra o app.py e confira USUARIO_BANCO e SENHA_BANCO
   (use os mesmos dados do seu MySQL)

4) Rode:
   python app.py

5) Abra no navegador: http://localhost:5000

Telas:
- Início: mostra cada cômodo, sensores (última leitura) e atuadores (liga/desliga)
- Cômodos: adicionar, renomear e apagar
- Atuadores: adicionar, ligar/desligar e apagar
- Leituras: registrar, filtrar valores > 28, contar e apagar

Obs: ainda não tem login, o usuário 1 é usado direto.
