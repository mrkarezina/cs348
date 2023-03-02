This folder contains utility to format raw data sourced from the CIA factbook and creates copies that have been modified to be fed into the database within the services/web/data folder.

format_csv.py carries out this process over all csv files in the raw_data directory.

This procedure is kept seprate from the main service for now as it only needs to be conducted once a year when new data is included, so constant re-formatting whenever the container is built is avoided.

iso.csv sourced from https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv, altered to overlap with more country name formats provided by the CIA factbook.