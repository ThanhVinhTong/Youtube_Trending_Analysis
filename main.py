import sys, crawl, clean

if __name__ == '__main__':
	# crawl
	if '--crawl' in sys.argv:
		crawl.main()
	# clean
	if '--clean' in sys.argv:
		clean.main()