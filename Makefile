SHELL:=/bin/bash

all:
	@echo "choose explicit target = type 'make ' and press TAB"

S=scripts

# ===== MAIN STUFF 

SCRIPT=$S/comment_downloader.py

POST_ID=2547974552025942
MAX_COMMENTS=10
REPLIES=-r

OUT=out

download:
	python3 $(SCRIPT) -p $(POST_ID) -n $(MAX_COMMENTS) $(REPLIES) > $(OUT)

