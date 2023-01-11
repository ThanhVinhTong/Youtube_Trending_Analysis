import sys, crawl, clean, visualize

if __name__ == '__main__':
	# crawl
	if '--crawl' in sys.argv:
		crawl.main()

	# clean
	if '--clean' in sys.argv:
		clean.main()

	# visualize
	data = clean.read()
	if sys.argv[1] == '1':
		visualize.plot_1(data)
	elif sys.argv[1] == '2':
		visualize.plot_2(data)
	elif sys.argv[1] == '3':
		# TODO
		pass
	elif sys.argv[1] == '4':
		# TODO
		pass
	elif sys.argv[1] == '5':
		visualize.plot_5(data)
	else:
		print('No plot code selected')