# str.isdigit():用来判断字符串是否全部用数字组成；
# Str.replace('str1', 'str2'):用来将字符串中所有的str1替换成str2；
# and判断，对于出现为假可能性高的放在前面，将查询步骤复杂的放在后面


def is_isbn_or_key(word):
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-','')
    if '-' in word and len(short_word) == 10 and short_word.isdigit:
        isbn_or_key = 'isbn'
    return isbn_or_key