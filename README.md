# moodle_report

Descubra os estudantes que não estão participando das aulas no Moodle

## Dependências:

- flask (para interface web)
- gunicorn (para o Heroku)


## Exemplo de uso (linha de comando):

    $ chmod +x moodle_report.py
    $ ./moodle_report.py meu_arquivo_de_log_csv

** Relatório de uso **

-> Todos os usuários acessaram o Moodle ao menos uma vez.

-> Os seguintes usuários não submeteram nenhuma atividade no Moodle.
       CCCC

-> Número de acessos por usuário:
        AAAAA: 5
        BBBBBB: 4
        CCCC: 2

-> Número de submissões por usuário:
        AAAAA: 5
        BBBBBB: 4
        CCCC: 0
