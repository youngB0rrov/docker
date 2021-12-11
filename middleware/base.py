class Middleware:
    # vs ji(в с джи ай) стандартный интерфейс для пайтоновских программ
    def __call__(self, environ, start_response):
        raise NotImplementedError
