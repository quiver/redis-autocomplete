# vim: set fileencoding=utf8
'''
zrange-based autocomplete

See "Redis in Action" Ch. 6.2 for details.
'''
import uuid
import redis
import sys

KEY = 'key'
word = '`abcdefghijklmnopqrstuvwxyz{'
r = redis.Redis(db=2)

def sentinel_before(w):
    last_char = w[-1]
    try:
        index = word.index(last_char)
        postfix = word[index-1]
        w = w[:-1] + postfix
    except Exception, err:
        print err
        pass
    return w + str(uuid.uuid4())

def sentinel_after(w):
    w = w + '}'
    return w + str(uuid.uuid4())

def add_word(query):
    r.zadd(KEY, word, 0)

def suggest(query):
    before = sentinel_before(query)
    after  = sentinel_after(query)
    r.zadd(KEY, **{ before : 0,
                    after  : 0,
                  })
    rank_before = r.zrank(KEY, before)
    rank_after  = r.zrank(KEY, after)
    matches = r.zrange(KEY, rank_before+1, rank_after-1)

    r.zrem(KEY, before, after) # cleanup

    return matches

def main():
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = 'python'
    print suggest(query)

if __name__ == '__main__':
    main()
