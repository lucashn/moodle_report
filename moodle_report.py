#! /usr/bin/env python3

import csv
import sys
from typing import List, Dict, Set, Tuple
from collections import defaultdict

COL_HORA, COL_NOME, COL_AFETADO, COL_EVENTO = 0, 1, 2, 5
EVENTO_INSCRICAO = "Usuário inscrito no curso"

def main():
    try:
        fname = sys.argv[1]
    except IndexError:
        print("Uso: {} nome_log.csv".format(sys.argv[0]))
        return
    
    try:
        enroled_users, access_by_user = get_participation_stats(fname)
        show_usage_report(enroled_users, access_by_user)
    except e:
        print("Erro ao processar arquivo de log. Arquivo inválido?")
        print(e)

def get_participation_stats(fname: str) -> Tuple[Set[str], Dict[str, int]]:
    enrolled_users : Set[str] = set()
    access_by_user : Dict[str, int] = defaultdict(int)

    with open(fname) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if is_enroll_event(row):
                enrolled_user_name = row[COL_AFETADO].upper()
                enrolled_users.add(enrolled_user_name)
            elif is_access_event(row):
                active_user_name = row[COL_NOME].upper()
                access_by_user[active_user_name] += 1
    
    return enrolled_users, access_by_user

def show_usage_report(enroled_users: Set[str], access_by_user: Dict[str, int]):
    active_users = set(access_by_user.keys())
    inactive_users = enroled_users - active_users
    usage_desc = sorted(access_by_user.items(), key=lambda x: x[1], reverse=True)

    print("** Relatório de uso **")
    print("\n-> Usuários que nunca entraram no Moodle:")
    for user in inactive_users:
        print("\t{}".format(user))
    
    print("\n-> Usuários por uso:")
    for user, count in usage_desc:
        print("\t{}: {}".format(user, count))

def is_enroll_event(row: List[str]):
    return row[COL_EVENTO] == EVENTO_INSCRICAO

def is_access_event(row: List[str]):
    return row[COL_NOME] != '-'

if __name__ == '__main__':
    main()