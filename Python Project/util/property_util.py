import configparser


class PropertyUtil:
    @staticmethod
    def get_property_string():
        config = configparser.ConfigParser()
        config.read('db.properties')

        hostname = config['DATABASE']['hostname']
        dbname = config['DATABASE']['dbname']
        username = config['DATABASE']['username']
        password = config['DATABASE']['password']
        port = config['DATABASE']['port']

        return {
            'host': hostname,
            'database': dbname,
            'user': username,
            'password': password,
            'port': port
        }
