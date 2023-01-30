import sys, crawl, merge_files

if __name__ == '__main__':
	# crawl
	if '--crawl' in sys.argv:
		crawl.main()

	# merge files
	if '--merge_files' in sys.argv:
		merge_files.main()