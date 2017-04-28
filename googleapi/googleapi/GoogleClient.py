import pprint
from googleapiclient.discovery import build


class GoogleClient:
    key = "AIzaSyD5BYgxBrUFtDAlnAYvhpNhEFxrtdF2LHc"
    customEngine = '017834202398449870076:eeqbhmbsv90'

    def __init__(self):
        self.search = ''
        self.service = build("customsearch", "v1",
                             developerKey=self.key)



    def get_snippet(self,search):
        start = 1
        while True:
            res = self.service.cse().list(
                q='Ivan',
                cx=self.customEngine,
                start=str(start)
            ).execute()

            yield res

            start = start + 10
            if start>100:
                break
