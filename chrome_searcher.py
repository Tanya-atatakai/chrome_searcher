from sys import platform

import requests

if 'linux' in platform:
    platform_param = 'linux'
elif platform == "darwin":
    platform_param = 'mac'
else:
    platform_param = platform


def get_download_link():
    """
    Returns link for downloading google chrome browser with
    standalone and platform parameters
    """
    return 'https://www.google.ru/chrome/browser/thankyou.html?' \
           'standalone=1&platform={platform}'.format(platform=platform_param)


def request_version_data():
    """
    Requests and json-encodes data of google chrome versions
    from omahaproxy.appspot.com

    :return: version_data | print of error
    :rtype: list | str
    """
    version_data = None
    url = 'http://omahaproxy.appspot.com/all.json'
    response = requests.get(url)
    if response.status_code == 200:
        version_data = response.json()
    if version_data is None:
        print("Can't request version data from {url}. Please check this url or "
              "your network".format(url=url))
    else:
        return version_data


def get_latest_version():
    """
    Returns latest stable version of google chrome for this platform

    :return: latest_version or print of error
    :rtype: str | str
    """
    latest_version = None
    version_data = request_version_data()
    if version_data:
        for elements in version_data:
            if (elements.get('versions') and
                    elements.get('os') == platform_param):
                for element in elements.get('versions'):
                    if element.get('channel') == 'stable':
                        latest_version = element.get('version')
    if latest_version is None:
        print("Can't get latest version of google chrome")
    else:
        return latest_version


if __name__ == '__main__':

    version = get_latest_version()
    download_link = get_download_link()

    if version:
        print('Latest google chrome version for {platform} platform: {version}'.
              format(platform=platform_param, version=version))

    print('Link for downloading google chrome:', download_link)
