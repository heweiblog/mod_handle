import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Example System Server")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--password", default="123", help='Use "env:" or "file:" prefix to specify source')
    parser.add_argument('--port', type=int, default=8300, help='Netconf server port')
    parser.add_argument("--username", default="heweiwei", help='Netconf username')
    args = parser.parse_args()
    print(args)
    print(args.username)

