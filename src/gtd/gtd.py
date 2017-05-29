

class Gtd(object):
    def __init__(self, db = None):
        self.db = db
        print('class Gtd initialized')

    def take_server_object(self, server_obj):
        self.server = server_obj

    def take_data(self,data):
        print("the proc got this data: {}".format(data))
        self.current_data = data

    def process(self):
        print('processing')
        pass

    def get_message_back_to_client(self):
        return_message = 'proc2client: ' + self.current_data
        print('this is the return_message: {}'.format(return_message))
        return return_message




