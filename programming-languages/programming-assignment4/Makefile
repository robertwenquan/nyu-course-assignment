all:	clean
	/bin/cp -f qw476.go qw476/src/unify/unify.go
	cd qw476/src/unify && go install

pkg:	all
	zip -T qw476.zip qw476/src/unify/unify.go

clean:	
	rm -fr qw476/bin *.zip

test:	all
	@echo "Testing programming assignment 4 ..."
	@./verify-case.sh

remote:	pkg
	scp -r qw476.zip *.sh testcases qw476@kimota.net:~/
