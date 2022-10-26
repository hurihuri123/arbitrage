import urllib.request
from abc import ABC, abstractmethod

class HTTP_CLIENT(ABC):
    @abstractmethod
    def get(url):
        return urllib.request.urlopen(url).read()


if __name__ == "__main__":
    print(HTTP_CLIENT.get("https://stackoverflow.com/"))
        
    