# vim: set fileencoding=utf8

'''
@antirez algorithm

http://oldblog.antirez.com/post/autocomplete-with-redis.html
'''
import redis
import sys

KEY = 'key'
TERMINAL = '*'
r = redis.Redis(db=3)

def add_word(word):
    pipeline = r.pipeline(True)
    for idx in range(1, len(word) + 1):
        r.zadd(KEY, word[:idx], 0)
    r.zadd(KEY, word + TERMINAL, 0)
    pipeline.execute()

def suggest(prefix):
    results = []
    rangelen = 50
    start = r.zrank(KEY, prefix)

    if not start:
        return results

    while True:
        for entry in r.zrange(KEY, start, start + rangelen):
            if not entry.startswith(prefix):
                return results

            if entry.endswith(TERMINAL):
                results.append(entry[:-1])
        start += rangelen
    return results


def main():
    if len(sys.argv) > 1:
        prefix = sys.argv[1]
    else:
        prefix = 'ba'
    print suggest(prefix)

if __name__ == '__main__':
    main()
