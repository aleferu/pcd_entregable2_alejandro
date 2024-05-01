#!/usr/bin/env bash

# Imprime qué comandos son utilizados y para en error
set -xe

# Generación del documento
pdflatex -jobname="49274537G-entregable2-pcd" main.tex

# Done
printf "\nDONE!\n"
