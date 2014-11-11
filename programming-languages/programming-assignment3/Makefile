all:	assignment3.hs
	ghc *.hs -o assignment3 && zip -T qw476.zip *.hs

clean:	
	rm -f *.o *.hi *.zip assignment3

test:	
	@echo "Testing programming assignment 3 ..."
	@./verify-case.sh

remote:	
	scp -r *.zip *.sh testcases qw476@kimota.net:~/
