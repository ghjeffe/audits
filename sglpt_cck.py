#!python3

from collections import namedtuple

def parse_svc_file():
    CSV_Parse = namedtuple('CSV_Parse', ['service'
                                        ,'acct_name'
                                        ,'acct_num'
                                        ,'bank_name'
                                        ,'bank_aba'
                                        ,'users'
                                        ]
                           )
    
    with open('samples/ServiceProfileReport07202016223214.CSV') as svc_rpt:
        for line in svc_rpt:
            line = line.strip('\n')
            try:
                parsed = CSV_Parse(*line.split('","'))
            except TypeError: #.split() throws TypeError if delimiter not found
                pass
            else:
                users = [user.strip('\n" ') for user in parsed.users.split(', ')]
                try:
                    users.remove('')
                except ValueError:
                    pass
                if len(users) > 0:
                    print(parsed.service, parsed.acct_name, parsed.users, sep='||')
                    
def parse_users():
    pass
    
def main():
    pass