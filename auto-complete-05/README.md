Inverted Index Implementation

http://patshaughnessy.net/2011/11/29/two-ways-of-using-redis-to-build-a-nosql-autocomplete-search-index
http://en.wikipedia.org/wiki/Inverted_index

## import data

  ```
  $ python init_data.py
  ```

## suggest

  ```
  $ python suggest.py wal
  i am the walrus
  winston's walk
  $ python suggest.py wal am
  i am the walrus
  ```

