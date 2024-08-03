# TEST = True    # Режим для тестов
TEST = False  # Режим запуска программы

if TEST:
	import tests.settingsTest
	#import tests.content.subgamesTest
	#import lib.bslib
else:
	from src.main import *
	main()