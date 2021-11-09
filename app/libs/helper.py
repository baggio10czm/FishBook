def is_isbn_or_key(word):
    """
    :param word: API传进来参数
    判断参数是isbn or 关键字
    isbn 有两种情况:
    13位全部是数字 / 10位带'-'的数字
    isdigit() 检测字符串是否都由数字组成
    """
    if len(word) == 13 and word.isdigit():
        return 'isbn'
    newWord = word.replace('-', "7")
    if '-' in word and len(newWord) == 10 and newWord.isdigit():
        return 'isbn'
    return 'key'

