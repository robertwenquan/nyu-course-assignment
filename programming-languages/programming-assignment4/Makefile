all:	clean
	zip -T qw476.zip qw476/src/unify/unify.go

clean:	
	rm -fr qw476/bin *.zip

test:	
	@echo "Testing programming assignment 4 ..."
	rm -fr qw476/bin
	cd qw476/src/unify && go install
	@./verify-case.sh

remote:	all
	scp -r qw476.zip *.sh testcases qw476@kimota.net:~/
