# vim: set fileencoding=utf8

import suggest

with open('/usr/share/dict/words') as fp:
    try:
        for line in fp:
            word = line.strip().lower()
            suggest.add_word(word)
    except Exception, err:
        print err
