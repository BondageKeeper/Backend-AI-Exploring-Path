#But if we turn on our container our FastApi will try to connect with PostgreSQL and as we know our database has a localhost
#and localhost will resemble this container , not our true computer(device) and; therefore FastApi won't recognize PostgreSQL
#which was launched on our Windows . We ended up having mistake about database connection

#in summary we have to use tool Docker Compose which is able to accept two container simultaneously(one for FastAPI and another for
#PostgreSQL) and Docker Compose automatically creates a network between them
#here is step-by-step plan:

#1)docker-compose.yml  this is a main instruction(here we launch our backend service from our DockerFile and database service from
#ready official pattern PostgresSQL

#2)DATABASE_URL instead of address 127.0.0.1 , In our settings of db we will write a name of the service of the database
#from compose file

#2)docker compose up - the most important command because it combines an assembly and a launch and a network and does all raw work for us
#docker compose up --build
