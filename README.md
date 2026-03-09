# inventory-analysis-sql
SQL and python project analyzing daily inventory movements, including production, transfers, and consumption.

Extracts of project developed in 2023 for a small business needing to controll and track daily inventory accross multiple production sites and sale points.

This connected a tkinter user interface to a local sqlite data base. Althought the main business need was a daily snapshot of movements and inventory in each sales branch, detail is kept of each transfer, then an sqlite database was considered as the best approach for scalabilty (due to the number of records to be written). The tkinter interface feautred a way to manually enter or load the inputs of movements and a reporting module, not included for confidenciality reasons.

In this project you can view some of the functions used in the app, the main query for daily snapshots and schema for the database.
