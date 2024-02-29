class Logger:
    @staticmethod
    def newline():
        print()

    @staticmethod
    def info(msg: str, *args, **kwargs):
        print("[+]", msg, *args, **kwargs)

    @staticmethod
    def err(msg: str, *args, **kwargs):
        print("[!]", msg, *args, **kwargs)
