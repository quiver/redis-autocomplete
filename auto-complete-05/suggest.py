# vim: set fileencoding=utf8
'''
RubyGem soulmate's autocomplete algorithm
or interved index algorithm

http://patshaughnessy.net/2011/11/29/two-ways-of-using-redis-to-build-a-nosql-autocomplete-search-index
http://en.wikipedia.org/wiki/Inverted_index

$ python suggest.py com
here comes the sun
so how come (no one loves me)
lend me your comb
come and get it
come together

$ python suggest.py com t
here comes the sun
come together
'''
import redis
import sys

r = redis.Redis(db=5)

def add_word(word):
    pipeline = r.pipeline(True)

    pipeline.incr('beatles:songid')
    song_id = pipeline.execute()[-1] 
    r.hmset('beatles:songs:%d'%song_id, {'title':word, 'id':song_id})
    for w in word.split(' '):
        for idx in range(1, len(w) + 1):
            r.sadd('beatles:term:' + w[:idx], song_id)
    pipeline.execute()

def suggest(query, ttl=600):
    query = sorted(query)
    results = []

    if not query:
        return results

    terms = ['beatles:term:' + term for term in query]
    r.sinterstore('beatles:query:' + '|'.join(query), *terms)
    r.expire('beatles:query:' + '|'.join(query), ttl)

    for song_id in r.smembers('beatles:query:' + '|'.join(query)):
        title = r.hget('beatles:songs:%s'%song_id, 'title')
        if title:
            results.append(title)

    return results

def main():
    if len(sys.argv) > 1:
        query = sys.argv[1:]
    else:
        query = ['the']

    for title in suggest(query):
        print title

if __name__ == '__main__':
    main()
