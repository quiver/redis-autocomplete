# vim: set fileencoding=utf8
'''
import The Beatles song titles
'''
import suggest

with open('song.txt') as fp:
    for line in fp:
        title = line.strip().lower()
        suggest.add_word(title)
