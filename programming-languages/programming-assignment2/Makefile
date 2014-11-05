all:	assignment2.adb
	gnatmake *.adb -o assignment2 && zip -T qw476.zip *.adb

clean:	
	rm -f *.o *.ali *.zip assignment2

test:	
	@echo "Testing programming assignment 2 ..."
	@./verify-case.sh

remote:	
	scp -r *.zip *.sh testcases qw476@kimota.net:~/
