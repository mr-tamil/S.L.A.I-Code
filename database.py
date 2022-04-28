# Version 0.2
import os
import sqlite3
import numpy


class Database:
    def __init__(self, file_name):
        self.conn = None
        self.file_name = r"{}".format(file_name)
        self.connect()

        self.close()

    def connect(self):
        self.conn = sqlite3.connect(self.file_name)

    def close(self):
        self.conn.commit()
        self.conn.close()

    # create table
    def create_table(self, name, cols):
        self.connect()
        c = self.conn.cursor()

        # creating table
        cmd = f"CREATE TABLE {name} ("
        for i in range(len(cols)):
            cmd += f"{cols[i][0]} {cols[i][1]}, "
        cmd = cmd[:-2] + ')'

        try:
            c.execute(cmd)
            self.close()
            status = True

        except:
            status = False

        data = {"status": status,
                "type": "create table",
                "rowcount": c.rowcount,
                "table": name,
                "value": cols,
                "command": cmd}
        return data

    # insert one value into the table
    def insert(self, table, values=None):
        self.connect()
        c = self.conn.cursor()
        cmd = f"INSERT INTO {table} VALUES ("

        query = None
        i = 0
        for value in values:
            if i == 0:
                cmd += '?'
                i = 1
            else:
                cmd += ',?'

        cmd += ')'
        c.execute(cmd, values)
        self.close()
        data = {"status": True,
                "type": "insert",
                "rowcount": c.rowcount,
                "table": table,
                "value": values,
                "command": cmd}
        return data

    # insert one or more values into the table
    def insert_many(self, table, values):
        self.connect()
        c = self.conn.cursor()

        cmd = f"INSERT INTO {table} VALUES ("
        no_cols = len(values[0])
        cmd = cmd + '?, ' * no_cols
        cmd = cmd[:-2] + ')'

        c.executemany(cmd, values)
        self.close()

        data = {"status": True,
                "type": "insert many",
                "rowcount": c.rowcount,
                "table": table,
                "values": values,
                "command": cmd}
        return data

    # update the table
    def update_table(self, table, from_, to, like='='):
        cols_original, data_original = from_
        cols_update, data_update = to

        self.connect()
        c = self.conn.cursor()

        if type(data_update) == str:
            last = f'{cols_original} {like} \'{data_original}\''
        else:
            last = f'{cols_original} {like} {data_original}'

        if type(data_update) == str:
            first = f'{cols_update} = \'{data_update}\''
        else:
            first = f'{cols_update} = {data_update}'

        cmd = f"UPDATE {table} SET " + first + " WHERE " + last
        c.execute(cmd)

        self.close()

        updates = {"cols_original": cols_original,
                   "data_original": data_original,
                   "cols_update": cols_update,
                   "data_update": data_update}

        data = {"status": True,
                "type": "insert many",
                "rowcount": c.rowcount,
                "table": table,
                "updates": updates,
                "command": cmd}
        return data

    # delete from the table
    def delete(self, table, cols, data, like='='):
        self.connect()
        c = self.conn.cursor()

        if type(cols) == str:
            last = f'{cols} {like} \'{data}\''
        else:
            last = f'{cols} {like} {data}'
        cmd = f"DELETE FROM {table} WHERE " + last
        c.execute(cmd)

        self.close()
        data = {"status": True,
                "type": "delete",
                "rowcount": c.rowcount,
                "table": table,
                "values": {"cols": cols,
                           "data": data,
                           "like": like},
                "command": cmd}
        return data

    # delete the table
    def drop_table(self, table):
        self.connect()
        c = self.conn.cursor()

        cmd = f"DROP TABLE {table}"
        c.execute(cmd)

        self.close()
        data = {"status": True,
                "type": "drop table",
                "rowcount": c.rowcount,
                "table": table,
                "values": None,
                "command": cmd}
        return data

    # get data from the table with data
    def table_data_info(self, table, count=0, period=None, rowid=True, order=None):
        self.connect()
        c = self.conn.cursor()

        c.execute(f"PRAGMA TABLE_INFO ('{table}')")

        cols = [i[1] for i in c]

        if not rowid:
            cmd = f"SELECT * FROM {table}"

        else:
            cmd = f"SELECT rowid, * FROM {table}"
            cols.insert(0, "rowid")

        if order is not None:
            cmd += f' ORDER BY {order[0]} {order[1]}'

        c.execute(cmd)

        data = []
        if period is None:
            for i in c.fetchmany(count):  # Todo: Make simple using only c
                data.append(i)

        else:
            start = 1
            for i in c.fetchall():
                if period[0] <= start <= period[1]:
                    data.append(i)
                start += 1

        get_data = {"status": True,
                    "type": "get data",
                    "rowcount": c.rowcount,
                    "table": table,
                    "cols": cols,
                    "data": data,
                    "command": cmd}

        self.close()
        return get_data

    # get data from the table
    def table_data(self, table, search= None, like= None, condition= None, cols= False, count=0, period=None, rowid=True, order=None):
        self.connect()
        c = self.conn.cursor()
        data = []
        if cols:
            c.execute(f"PRAGMA TABLE_INFO ('{table}')")
            cols = [i[1] for i in c]

        if search is not None:
            arr = numpy.array(search)
            if arr.ndim == 1:
                search_cmd = f" WHERE {search[0]} {like} {search[1]}"
            else:
                search_cmd = " WHERE"
                length = len(arr)
                for i in range(length):
                    if i == length-1:
                        search_cmd += f" {arr[i][0]} {like[i]} {search[i][1]}"
                    else:
                        search_cmd += f" {arr[i][0]} {like[i]} {search[i][1]} {condition[i]}"

        if not rowid:
            cmd = f"SELECT * FROM {table}"
            if search is not None:
                cmd += search_cmd
        else:
            cmd = f"SELECT rowid, * FROM {table}"
            if search is not None:
                cmd += search_cmd

            if cols:
                cols.insert(0, "rowid")

        if order is not None:
            cmd += f' ORDER BY {order[0]} {order[1]}'

        if cols:
            data.append(cols)

        c.execute(cmd)
        if period is None:
            data.extend(c.fetchmany(count))
        else:
            start = 1
            for i in c.fetchall():
                if period[0] <= start <= period[1]:
                    data.append(i)
                start += 1

        self.close()

        return data

    # access info of the database
    def info(self):
        self.connect()
        c = self.conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = []
        for t in c:
            tables.append(t[0])

        info_data = []
        for i in range(len(tables)):
            table_name = tables[i]
            c.execute(f"PRAGMA TABLE_INFO ('{table_name}')")

            cols = [[i[0], i[1], i[2]] for i in c]
            table = {"table": table_name,
                     "cols": cols}
            info_data.append(table)

        get_data = {"status": True,
                    "type": "access data",
                    "rowcount": c.rowcount,
                    "tables": tables,
                    "info": info_data,
                    "command": None}
        self.close()

        return get_data

    # get tables list
    def tables(self):
        self.connect()
        c = self.conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = []
        for t in c:
            tables.append(t[0])

        self.close()

        return tables

    # get tables info
    def tables_info(self):
        self.connect()
        c = self.conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = []
        for t in c:
            tables.append(t[0])

        info_data = {}
        for i in range(len(tables)):
            table_name = tables[i]
            c.execute(f"PRAGMA TABLE_INFO ('{table_name}')")

            cols = [[i[0], i[1], i[2]] for i in c]
            info_data.update({table_name: cols})

        self.close()

        return info_data

    # get specific table info
    def table_info(self, table):
        self.connect()
        c = self.conn.cursor()
        c.execute(f"PRAGMA TABLE_INFO ('{table}')")

        cols = [[i[0], i[1], i[2]] for i in c]
        self.close()

        return cols

    # query data by custom command
    def query(self, cmd):
        self.connect()
        c = self.conn.cursor()
        c.execute(cmd)
        data = c

        return data


if __name__ == "__main__":
    pass
    # connect or create database
    # db = Database(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Testing.db"))

    # create table
    # data = db.create_table("Neurons", [["neuron_id", "text"], ["neuron_name","text"]])

    # insert one value into the database
    # data = db.insert("Neurons", ["NC01234567890123405", "Greetings"])

    # insert one or more values into the database
    # data = db.insert_many("Neurons", [["NC01234567890123450", "Hi"],["NC01234567890123459", "Hello"]])

    # get data from the table
    # data = db.table_data("Neurons")

    # update the table
    # data = db.update_table("Neurons",from_= ["neuron_id", "NC01234567890123405"], to= ["neuron_name", "Hey"], like= "=")

    # access info of the database
    # data = db.info()

    # get tables list
    # data = db.tables()

    # get tables info
    # data = db.tables_info()

    # get specific table info
    # data = db.table_info("Neurons")

    # get data from the table with info
    # data = db.table_data_info("Neurons", count=2, rowid=False, period=[2, 3], order=["neuron_id", "desc"])

    # delete from the table
    # data = db.delete("Neurons", "neuron_name", "Hi")

    # delete the table
    # data = db.drop_table('Neurons')

    # query data by custom command
    # db.query("""Create Table system ('property' 'text', 'data' 'text')""")
    # db.close()

    # print(data)
