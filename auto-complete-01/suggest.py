# vim: set fileencoding=utf8
'''
prefix-match based autocomplete

See Redis in Action Ch.6.1 for details.
'''
import redis
import sys

LIMIT = 100
KEY = 'key' 
r = redis.Redis(db=1)

def add_word(word):
    r.lrem(KEY, word)
    r.lpush(KEY, word)
    r.ltrim(KEY, 0, LIMIT - 1)

def suggest(query):
    matches = []
    for name in r.lrange(KEY, 0, -1):
        if name.lower().startswith(query):
            matches.append(name)
    return matches

def main():
    if len(sys.argv) > 1:
        prefix = sys.argv[1]
    else:
        prefix = 'ba'
    print suggest(prefix)

if __name__ == '__main__':
    main()
