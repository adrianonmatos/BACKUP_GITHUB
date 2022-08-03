#!/usr/bin/bash
parent_directory="/home/adrianomatos/PROJETOS/crawler_fns"

# Saves file descriptors so they can be restored to whatever they were before redirection or used
# themselves to output to whatever they were before the following redirect.
exec 3>&1 4>&2
# Restore file descriptors for particular signals. Not generally necessary since they should be
# restored when the sub-shell exits.
trap 'exec 2>&4 1>&3' 0 1 2 3
# Redirect stdout to file log.out then redirect stderr to stdout. Note that the order is important
# when you want them going to the same file. stdout must be redirected before stderr is redirected
# to stdout.
exec 1>"$parent_directory/log.out" 2>&1

# Põe a data atual no log
date +"%D %T">>"$parent_directory/log.out"
echo "Start of execution">>"$parent_directory/log.out"

# Ativa o ambiente virtual
source "$parent_directory/VENV_FNS_Crawler/bin/activate"
# Baixa os novos arquivos
"$parent_directory/VENV_FNS_Crawler/bin/python3.10" "$parent_directory/crawlerFNS.py" 2021 2022

date +"%D %T">>"$parent_directory/log.out"
echo "End of execution">>"$parent_directory/log.out"
