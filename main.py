import sys, crawl, clean, visualize

if __name__ == '__main__':
	# crawl
	if '--crawl' in sys.argv:
		crawl.main()

	# clean
	if '--clean' in sys.argv:
		clean.main()

	# visualize
	if sys.argv[1] == '1':
		data = clean.read()
		visualize.plot_1(data)
	elif sys.argv[1] == '2':
		data = clean.read()
		visualize.plot_2(data)
	elif sys.argv[1] == '3':
		data = clean.read()
		visualize.plot_3(data)
	elif sys.argv[1] == '4':
		data = clean.read()
		visualize.plot_4(data)
	else:
		print('No plot code selected')