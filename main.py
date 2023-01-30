import sys, crawl, merge_files, visualize

if __name__ == '__main__':
	# crawl
	if '--crawl' in sys.argv:
		crawl.main()

	# merge files
	if '--merge_files' in sys.argv:
		merge_files.main()

	# visualize
	if sys.argv[1] == '1':
		data = merge_files.read()
		visualize.plot_1(data)
	elif sys.argv[1] == '2':
		data = merge_files.read()
		visualize.plot_2(data)
	elif sys.argv[1] == '3':
		data = merge_files.read()
		visualize.plot_3(data)
	elif sys.argv[1] == '4':
		data = merge_files.read()
		visualize.plot_4(data)
	else:
		print('No plot code selected')