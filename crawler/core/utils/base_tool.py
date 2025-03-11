
__all__ = ['auto_backend_wrapper', "get_all_attribute_words"]

from bs4 import BeautifulSoup

import functools

def auto_backend_wrapper(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if hasattr(self, "save") and callable(getattr(self, "save")):
            self.save(result)
        if hasattr(self, "quit") and callable(getattr(self, "quit")):
            self.quit()
        return result
    return wrapper

def get_all_attribute_words(tbody, results=[]):
    """
    tbody: html element
    results: original results(list)

    將tbody中的文字轉換成str(文字)以list形式返回
    return list(str)
    """

    #html_content = tbody.get_attribute("innerHTML")

    _results = results
    soup = BeautifulSoup(tbody, "html.parser")
    for row in soup.find_all("tr"):
        th = row.find("th")
        td = row.find("td")

        if th and td:
            label = th.get_text(strip=True)
            value = td.get_text(strip=True)
            img_tag = td.find("img")

            if img_tag and img_tag.has_attr("src"):
                value = img_tag["src"]
            else:
                a_tag = td.find("a")
                if a_tag and a_tag.has_attr("href"):
                    value = a_tag["href"]

            _results.append(f"\t{label}:\t{value}")
        row.decompose()

    for text in soup.stripped_strings:
        _results.append((f"\t{text}"))

    for img in soup.find_all("img"):
        img_url = img.get("src")
        _results.append((f"\t圖片連結:\t{img_url}"))

    _results.append(("\n"))
    return _results