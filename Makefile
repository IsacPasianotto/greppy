init:
		./setup.sh

PHONY: clean

clean:
		rm *.txt
		rm -f profile.*
		rm -f utils/*.html
		rm -f utils/*.c
		rm -f utils/*.so
		rm -rf build
