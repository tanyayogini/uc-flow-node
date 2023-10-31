from enum import Enum

class NodeAction(str, Enum):
    auth = 'auth'
    upload_file = 'upload_file'
    get_file_list = 'get_file_list'
