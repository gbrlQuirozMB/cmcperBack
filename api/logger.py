import logging as log

# log.basicConfig(level=log.INFO)
log.basicConfig(
                # format="%(asctime)s - %(levelname)s [%(filename)s:%(lineno)s]-> %(message)s",
                format="%(asctime)s - %(levelname)s [%(pathname)s:%(lineno)s]-> \n %(message)s",
                datefmt="%Y-%m-%d %H:%M",
                handlers=[
                    log.FileHandler("errores.log"),
                    log.StreamHandler()
                ],
                level=log.DEBUG)

# log.info(__name__)  # si se ejecuta este archivo imprime __main__ si se ejecuta desde otro archivo es logger
if __name__ == "__main__": #revisa si se esta ejecutando desde aqui __name__
    log.debug("este es un debug")
    log.info("este es un info")
    log.warning("este es un warning")
    log.error("este es un error")
    log.critical("este es un critical")