# Sistema de Gerenciamento de Eventos
Aplicação Django para gerenciamento de eventos, usando PostgreSQL.

Passos para rodar
1. Instale as dependências
   ```
   pip install -r requirements.txt
   ```
2. Crie e Configure na raiz do projeto o arquivo .env
   ```env
   DATABASE_NAME=seu_banco
   DATABASE_USER=seu_usuario
   DATABASE_PASS=sua_senha
   DATABASE_HOST=localhost
   DATABASE_PORTT=5432
   ```
3. Rode as migrações
  ```bash
    python manage.py migrate
  ```
4. Inicie o Servidor
   ```bash
   python manage.py runserver
   ```
