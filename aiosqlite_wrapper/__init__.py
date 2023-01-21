import aiosqlite, sys, datetime

class FileTypeError(Exception):
    pass

class database():
    """
    database
    ----------
    starts a database instance
    """

    def __init__(self, path_to_database: str, list_or_tuple: bool=True, error_raise=True, log_path: str=None):
        has_ending         = path_to_database.endswith('.sqlite')
        if has_ending is False:
            self.db        = f'{path_to_database}.sqlite'
        elif has_ending is True:
            self.db        = path_to_database
        self.db_name       = path_to_database
        if log_path:
            if not log_path.endswith(('.txt', '.log')):
                raise FileTypeError('log file must end with .txt or .log')
            with open(log_path, 'a+') as f:
                f.write(f'{datetime.datetime.now()} | database activated\n')
        self.log_path      = log_path
        self.list_or_tuple = list_or_tuple
        self.error_raise   = error_raise
        
    
    # UTILITIES

    # color text
    def color(self, text: str) -> str:
        return text

    # newline function
    def newline(self, n: int=1):
        """
        erase and go back to previous line
        """
        cursor = '\x1b[1A' 
        erase = '\x1b[2K' 
        for _ in range(n):
            sys.stdout.write(cursor)
            sys.stdout.write(erase)

    # tuple to list converter
    def tuple_to_list(self, tuple_item: tuple) -> list:
        """
        convert a tuple into a list
        """
        result = list(list(i) for i in tuple_item)
        # returning result as [[values], [values], [values]]
        return result

    # format an error
    def log(self, text: str) -> None:
        if self.log_path:
            with open(self.log_path, 'a+') as f:
                f.write(f'{datetime.datetime.now()} | {text}\n')

    
    # ERRORS AND ERROR HANDLING
    def handle_error(self, error: Exception) -> Exception:
        """
        return or raise an error
        """

        # log errors
        self.log(str(error))

        # check to see whether the user opted to raise the error or to return it
        if self.error_raise:
            raise error
        elif not self.error_raise:
            return f'error: {error}'

    # handle result data
    def handle_result(self, result: any) -> list:
        """
        handle a result to format it into list with either tuples or lists
        """
        # if the result is nothing return a success message
        if result == []:
            return 'query ok, no results'
        
        # format the result into either a tuple or a list
        if self.list_or_tuple is False:
            formatted_result = result
        elif self.list_or_tuple is True:
            formatted_result = self.tuple_to_list(result)

        final_result: list = []
        for i in formatted_result:
            if len(i) == 1:
                final_result.append(i[0])
            else:
                final_result.append(i)
        
        if len(final_result) == 1:
            return final_result[0]

        return final_result

    # REGULAR

    # create a db
    def create(self) -> str:
        """
        create
        ----
        creates the database, and defines the path
        """
        
        with open(self.db, 'a+'):
            self.log(f'created database at {self.db}')
            return f'succesfully initialised database under {self.db}'

    # execute a query
    async def execute(self, query: str, file_path: str=None, format: bool=True) -> list:
        """
        execute
        -------
        one of the main queries within the module. execute any query using one function, or use the built in functions to make data fetching easier.

        """

        # try statement so we catch errors
        try:
            # async with a connection
            async with aiosqlite.connect(self.db) as cursor:
                # execute the query
                exec = await cursor.execute(query)
                # fetch any results from the query
                result = await exec.fetchall()
                # commit the transaction
                await cursor.commit()
        except Exception as e:
            # handle errors
            return self.handle_error(e)
        
        if format:
            final_result = self.handle_result(result)
        elif not format:
            final_result = result

        if file_path:
            with open(file_path, 'a+') as file:
                file.write(str(final_result))
        
        self.log(f'executed: {query}')
        return final_result

    # fetch items
    async def fetch(self, table: str, items: str='*', file_path: str=None) -> list:
        """
        fetch
        -----
        fetch data from a table. column select defaults to all, but you can specify.
        
        example query:
        
        `await db.fetch('example_table', 'example_column, example_column')`

        optionally, you can also write this data into a file using the file_path paramater.
        example query with file_path:
        
        `await db.fetch('example_table', file_path='my_data.txt')`
        """
        # try statement so we catch errors
        try:
            # async with a connection
            async with aiosqlite.connect(self.db) as cursor:
                # execute the query
                exec = await cursor.execute(f'select {items} from {table}')
                # fetch any results from the query
                result = await exec.fetchall()
                # commit the transaction
                await cursor.commit()
        except Exception as e:
            # handle errors
            return self.handle_error(e)
        
        # handle the result so it gives back sanitized data
        final_result = self.handle_result(result)

        # if applicable write to a file
        if file_path:
            with open(file_path, 'a+') as file:
                file.write(str(final_result))
        
        self.log(f'fetched {items} from {table}')
        # return the final result
        return final_result

    # fetch items
    async def get(self, table: str, where: str, items: str='*', file_path: str=None) -> list:
        """
        fetch
        -----
        fetch data from a table. column select defaults to all, but you can specify.
        
        example query:
        
        `await db.fetch('example_table', 'example_column, example_column')`

        optionally, you can also write this data into a file using the file_path paramater.
        example query with file_path:
        
        `await db.fetch('example_table', file_path='my_data.txt')`
        """
        # try statement so we catch errors
        try:
            # async with a connection
            async with aiosqlite.connect(self.db) as cursor:
                # execute the query
                exec = await cursor.execute(f'select {items} from {table} where {where}')
                # fetch any results from the query
                result = await exec.fetchall()
                # commit the transaction
                await cursor.commit()
        except Exception as e:
            # handle errors
            return self.handle_error(e)
        
        # handle the result so it gives back sanitized data
        final_result = self.handle_result(result)

        # if applicable write to a file
        if file_path:
            with open(file_path, 'a+') as file:
                file.write(str(final_result))
        
        self.log(f'fetched {items} from {table} where {where}')
        # return the final result
        return final_result

    # insert items
    async def insert(self, table: str, values: list) -> str:
        """
        insert
        ------
        insert data into a table
        """

        # try statement so we catch errors
        try:
            # async with a connection
            async with aiosqlite.connect(self.db) as cursor:
                # variable that will return how many rows were added
                row_amount = 0
                # execute the query
                for i in values:
                    await cursor.execute(f"insert into {table} values(" + str(i) + ")")
                    row_amount += 1
                await cursor.commit()

        except Exception as e:
            # handle errors
            return self.handle_error(e)

        # return the final result
        self.log(f'added {row_amount} rows into {table}')
        return f'query ok, {row_amount} rows affected'

    # delete a table
    async def drop(self, table):
        """
        drop
        ------
        delete a table from the database
        """

        # try statement so we catch errors
        try:
            # async with a connection
            async with aiosqlite.connect(self.db) as cursor:
                await cursor.execute(f'drop table {table}')

        except Exception as e:
            # handle errors
            return self.handle_error(e)

        # return the final result
        self.log(f'deleted table {table}')
        return f'query ok, deleted table {table}'

    # TERMINAL
    async def terminal(self, minimize=False):
        """
        terminal
        --------
        create a sqlite terminal instance

        WARNING: this will pause all other operations, 
        and you not be able to use any other functions 
        after calling this one.
        """
        self.error_raise = False
        self.terminal_instance = True

        print(self.color(f'sqlite terminal | {self.db}'))
        
        while True:
            query = input('- ')
            
            if minimize:
                self.newline(2)
            result = await self.execute(query)
            print(result)
