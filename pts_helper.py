import configparser

def get_pts(key: str) -> str:
    cfg = configparser.ConfigParser()
    cfg.read("pts_config.ini")
    devname = cfg["pts"][key]
    return devname
