import configparser
from Reddit.Api.Reddit import scrape_reddit
def main():
    config_file_path = "config.ini"
    config = configparser.ConfigParser()
    config.read(config_file_path)

    print("Ekleme işlemi başladı...")

    scrape_reddit(config['Reddit'], config['Database'])


if __name__ == "__main__":
    main()

