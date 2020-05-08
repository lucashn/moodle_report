#! /usr/bin/env python3

import csv
import sys
from typing import List, Dict, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass

COL_HORA, COL_NOME, COL_AFETADO, COL_EVENTO = 0, 1, 2, 5
EVENTO_INSCRICAO = "Usuário inscrito no curso"
EVENTO_ATIVIDADE_ENVIADA = "Um envio foi submetido."


@dataclass
class UserStats:
    num_access: int
    num_submissions: int


def main():
    try:
        fname = sys.argv[1]
    except IndexError:
        print("Uso: {} nome_log.csv".format(sys.argv[0]))
        return

    try:
        enroled_users, access_by_user = get_participation_stats(fname)
        show_usage_report(enroled_users, access_by_user)
    except Exception as e:
        print("Erro ao processar arquivo de log. Arquivo inválido?")
        print(e)


def get_participation_stats(fname: str) -> Tuple[Set[str], Dict[str, UserStats]]:
    enrolled_users: Set[str] = set()
    stats_by_name: Dict[str, UserStats] = defaultdict(lambda: UserStats(0, 0))

    with open(fname) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if is_enroll_event(row):
                enrolled_user_name = row[COL_AFETADO].upper()
                enrolled_users.add(enrolled_user_name)
            else:
                active_user_name = row[COL_NOME].upper()
                
                if is_access_event(row):
                    stats_by_name[active_user_name].num_access += 1

                if is_submit_event(row):
                    stats_by_name[active_user_name].num_submissions += 1

    return enrolled_users, stats_by_name


def is_submit_event(row: List[str]):
    return row[COL_EVENTO] == EVENTO_ATIVIDADE_ENVIADA


def is_enroll_event(row: List[str]):
    return row[COL_EVENTO] == EVENTO_INSCRICAO


def is_access_event(row: List[str]):
    return row[COL_NOME] != '-'


def show_usage_report(enroled_users: Set[str], stats_by_name: Dict[str, UserStats]):
    active_users = set(stats_by_name.keys())
    inactive_users = enroled_users - active_users

    print("** Relatório de uso **\n")
    report_names(inactive_users,
           "Os seguintes usuários não acessaram o Moodle:",
           "Todos os usuários acessaram o Moodle ao menos uma vez.")

    users_without_submissions = [name for name, stats in stats_by_name.items() if stats.num_submissions == 0]
    report_names(users_without_submissions,
           "Os seguintes usuários não submeteram nenhuma atividade no Moodle",
           "Todos os usuários submeteram ao menos uma atividade no Moodle.")

    report_values(stats_by_name, "num_access", "Número de acessos por usuário:")
    report_values(stats_by_name, "num_submissions", "Número de submissões por usuário:")


def report_names(names: List[str], msg_true: str, msg_false: str):
    if names:
        print("-> " + msg_true)
        for name in sorted(names):
            print("\t{}".format(name))
    else:
        print("-> " + msg_false)
    print()

def report_values(stats_by_name: Dict[str, UserStats], attr: str, msg: str):
    print("-> " + msg)
    values = ((name, getattr(stats, attr) ) for name, stats in stats_by_name.items())
    sorted_values = sorted(values, key=lambda x: x[1], reverse=True)

    for name, val in sorted_values:
        print(f"\t-> {name}: {val}")
    print()

if __name__ == '__main__':
    main()
