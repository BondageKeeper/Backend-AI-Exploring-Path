#so for what do we need this library so badly?
#let's just imagine that we need to add new column in already-existing table and
#we have two ways:
#first: drop the table and create a new one(but in this case we will lose all data - we will be fired:)
#second: write all code in SQL which is uncomfortable and for community works - very inefficient
#so in such cases we have Alembic!
#this library simply compares two tables:what was created a long time ago(initial table) and what was created now(new table)
#and if it sees the difference(new column) - it generates a special script of migration
#we launch the script and Alembic carefully WITHOUT DELETING OLD DATA adds new column to the old database - perfect!
#'alembic init migration_folder' - we write it in terminal(file of db-config)

#'alembic revision --autogenerate -m "Initial migration"' - when models are written but table is empty we ask Alembic
#to fix changes / "Initial migration" - this is just a comment(a name of our migration)
#--autogenerate - comfortable flag which automatically compares python and tables in Postgres and writes a code of the change
#after that we write:
#'alembic upgrade head' - Alembic will just be connected with our table in Postgres and also it will create a service table
#(in this service table alembic will marker store a market of current database version - to know on what stage the project is

#let's say our migrations were stupid and we just don't like them and want to return the initial database view
#so , in that case we write in terminal: 'alembic downgrade -1' (one step behind)
# 'alembic downgrade base': return to the initial migration(drop all previous migrations)

#in the file of migration we might have LOTS OF , so if we want to now the gradual history of their creation we simply write
#'alembic history --indicate-current' - and we have got a history


'''So here I just wanna write a layout how to use alembic with sqlalchemy'''
'''alembic init migration_folder''alembic init migration_folder'''
'''alembic revision --autogenerate -m [Write here your annotation]'''
'''alembic upgrade head'''
