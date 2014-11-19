all:	qw476.hs
	ghc qw476.hs

clean:	
	rm -f *.o *.hi qw476

test:	
	@echo "Testing programming assignment 3 ..."
	@./verify-case.sh

remote:	
	scp -r qw476.hs *.sh testcases qw476@kimota.net:~/
