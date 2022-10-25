from argparse import ArgumentParser
from api.utils.utils import init_superuser
from asyncio import get_event_loop
from api.security.authentification_user import get_password_hash

if __name__ == '__main__':
    parser = ArgumentParser(description="Create superuser for first start service")
    parser.add_argument("--login", "-l", action="store", dest='login', help="Enter superuser login", required=False)
    parser.add_argument("--password", "-p", action="store", dest='password', help="Enter superuser password", required=False)
    parser.add_argument("--password_hash", "-ph", action="store", dest='password_hash', help="Get password hash", required=False)
    args = parser.parse_args()
    if args.login and args.password:
        loop = get_event_loop()
        loop.run_until_complete(init_superuser(args.login, args.password))
    if args.password_hash:
        print(get_password_hash(args.password_hash))
    if not args.password:
        print("Enter superuser password")
    if not args.login:
        print("Enter superuser login")


