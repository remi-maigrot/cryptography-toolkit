#!/usr/bin/env python3

##
## EPITECH PROJECT, 2023
## B-CNA-500-BDX-5-1-cryptography-remi.maigrot
## File description:
## main
##

from src.manage_algos import ManageAlgos
import sys

def do_PGP() -> None:
    algo = ManageAlgos()
    algo.manage_parsing()
    algo.launch()

if __name__ == "__main__":
    do_PGP()
