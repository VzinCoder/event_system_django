Sistema de Gerenciamento de Eventos
===================================

Sistema desenvolvido com Django e PostgreSQL para o gerenciamento de eventos.

Configuração do Ambiente
------------------------

1. Crie um ambiente virtual:
    

```bash
python -m venv venv
```

2. Ative o ambiente virtual:
    

* No Windows:
    
    ```bash
    venv\Scripts\activate
    ```
    
* No Linux/Mac:
    
    ```bash
    source venv/bin/activate
    ```
    

3. Instale as dependências:
    

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
    

Utilize o arquivo `.env.sample` localizado na pasta principal do projeto (onde está o `settings.py`) como referência para criar seu próprio arquivo `.env`.

5. Aplique as migrações:
    

```bash
python manage.py migrate
```

6. Inicie o servidor:
    

```bash
python manage.py runserver
```

Licença
-------

Este projeto está licenciado sob a Licença MIT.
