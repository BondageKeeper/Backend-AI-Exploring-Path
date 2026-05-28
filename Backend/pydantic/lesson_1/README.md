# Introduction
pydantic is a library for checking types of date and dealing with them in Python
it is like a guard: for example let's just assume that some users send data(this data is coming as JSON)
so if user for example sent a bad word instead of age(or another parameter) - than pydantic blocks this requests
and it doesn't let it go further to break a code
also it cleans data (converting raw data('10') into clean data(10) - we don't even need to use int()
BaseModel - in this class we write a type of data(we create a scheme of data for our user)
