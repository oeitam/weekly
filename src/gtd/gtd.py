

class Gtd(object):
    def __init__(self, db = None):
        self.db = db
        print('class Gtd initialized')

    def take_server_object(self, server_obj):
        self.server = server_obj

    # take_data - used by the server to push the data it got from teh client
    # to the proc/gtd for processing
    def take_data(self,data):
        print("the proc got this data: {}".format(data))
        self.current_data = data

    # process function does/start the heavy lifting of interpreting
    # the request from teh client and pusing the info to the database
    def process(self):
        print('processing data from the client')
        pass

    # get_message_back_to_client - method used by
    def get_message_back_to_client(self):
        return_message = 'proc2client: ' + self.current_data # (just echo for now)
        print('this is the return_message: {}'.format(return_message))
        return return_message




