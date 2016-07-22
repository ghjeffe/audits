#!python3

from collections import namedtuple

SERVICES_SET = set()
USERS_SET = set()

def parse_svc_file():
    delim = '","'
    Service_Parser = namedtuple('Service_Parser', ['service'
                                                   ,'acct_name'
                                                   ,'acct_num'
                                                   ,'bank_name'
                                                   ,'bank_aba'
                                                   ,'users'
                                                  ]
                                )
    
    User_Parser = namedtuple('User_Parser', ['user_id'
                                             ,'lname'
                                             ,'fname'
                                             ,'status'
                                             ]
                             )
    
    with open('samples/service-report.csv') as svc_rpt:
        for line in svc_rpt:
            line = line.strip('\n')
            try:
                parsed_svc = Service_Parser(*line.split(delim))
            except TypeError: #.split() throws TypeError if delimiter not found
                pass
            else:
                if len(parsed_svc.service) < 10: #we've moved passed the service section of file and are now on to users, status, etc.
                    try:
                        parsed_user = User_Parser(*line.split(delim)[0:4]) #throw away empty fields beyond status
                    except TypeError:
                        pass
                    else:
                        USERS_SET.add(parsed_user)
                else:
                    if len(parsed_svc.users) > 0:
                        SERVICES_SET.add(parsed_svc)
    return (SERVICES_SET, USERS_SET)

def get_user_services(user):
    users_services = []
    for item in SERVICES_SET:
        users = [user.strip('\n" ') for user in item.users.split(', ')]
        if user in users:
            users_services.append((item[:-1])) #return service up to and not including user
    return users_services
    
def main():
    parse_svc_file()
    with open('Singlepoint-CCK.csv', mode='w', encoding='utf8') as fh:
        fh.write('User ID,First Name,Last Name,User Access\n')
        for user_item in USERS_SET:
            user_id = user_item.user_id.strip('"')
            user_services = get_user_services(user_id)
            line = '{},{},{}'.format(user_id, user_item.fname, user_item.lname)
            if user_services:
                for service in user_services:
                    fh.write(line + ',{}({}; {}; {}; {})\n'.format(service[0].strip('"'), *service[1:]))
            else:
                fh.write('{},{}\n'.format(line, 'Admin')) #admins won't have service access

if __name__ == '__main__':
    main()