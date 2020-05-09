#! /usr/bin/env python3

import csv
import sys
from typing import List, Dict, Set, Tuple, TextIO
from collections import defaultdict
from dataclasses import dataclass

COL_HORA, COL_NOME, COL_AFETADO, COL_EVENTO = 0, 1, 2, 5
EVENTO_INSCRICAO = "Usuário inscrito no curso"
EVENTO_ATIVIDADE_ENVIADA = "Um envio foi submetido."
EVENTO_QUESTIONARIO_ENTREGUE = "Tentativa do questionário entregue"


@dataclass
class UserStats:
    num_access: int
    num_submissions: int


def main():
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f"Uso: {sys.argv[0]} nome_log.csv")
        return

    try:
        with open(fname) as file:
            process(file)
    except Exception as e:
        print("Erro ao processar arquivo de log. Arquivo inválido?")
        print(e)

def process(file: TextIO):
    enroled_users, access_by_user = get_participation_stats(file)
    show_usage_report(enroled_users, access_by_user)

def get_participation_stats(file: TextIO) -> Tuple[Set[str], Dict[str, UserStats]]:
    enrolled_users: Set[str] = set()
    stats_by_name: Dict[str, UserStats] = defaultdict(lambda: UserStats(0, 0))
    
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

    remove_spies(enrolled_users, stats_by_name)

    return enrolled_users, stats_by_name

def remove_spies(enrolled_users: Set[str], stats_by_name: Dict[str, UserStats]):
    spies = set(stats_by_name.keys()) - enrolled_users
    for spy in spies:
        del stats_by_name[spy]


def is_submit_event(row: List[str]):
    return row[COL_EVENTO] in (EVENTO_ATIVIDADE_ENVIADA, EVENTO_QUESTIONARIO_ENTREGUE)


def is_enroll_event(row: List[str]):
    return row[COL_EVENTO] == EVENTO_INSCRICAO


def is_access_event(row: List[str]):
    return row[COL_NOME] != '-'


def show_usage_report(enroled_users: Set[str], stats_by_name: Dict[str, UserStats]):
    active_users = set(stats_by_name.keys())
    inactive_users = enroled_users - active_users

    print("** Relatório de uso **\n")
    report_names(list(inactive_users),
           "Os seguintes usuários não acessaram o Moodle:",
           "Todos os usuários acessaram o Moodle ao menos uma vez.")

    users_without_submissions = [name for name, stats in stats_by_name.items() if stats.num_submissions == 0]
    report_names(users_without_submissions,
           "Os seguintes usuários não enviaram atividades ou questionários.",
           "Todos os usuários enviaram ao menos uma atividade ou questionário.")

    report_values(stats_by_name, "num_access", "Número de acessos por usuário:")
    report_values(stats_by_name, "num_submissions", "Número de envios por usuário:")


def report_names(names: List[str], msg_true: str, msg_false: str):
    if names:
        print("-> " + msg_true)
        for name in sorted(names):
            print(f"\t{name}")
    else:
        print("-> " + msg_false)
    print()

def report_values(stats_by_name: Dict[str, UserStats], attr: str, msg: str):
    print("-> " + msg)
    values = ((name, getattr(stats, attr) ) for name, stats in stats_by_name.items())
    sorted_values = sorted(values, key=lambda x: x[1], reverse=True)

    for name, val in sorted_values:
        print(f"\t{name}: {val}")
    print()

if __name__ == '__main__':
    main()
