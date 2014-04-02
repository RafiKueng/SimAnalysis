# all makes only diff, so the make file behaves as created by PS
# update updates the files provided on my server

# $BEFORE is the latex file to diff the current version to
# to be overwritten by command line
# make BEFORE=other-file.tex
BEFORE=ms-before.tex

all: main

clean:
	rm -f *.aux *.log *.bbl *.blg *~

diff:
	latexdiff $(BEFORE) ms.tex > msdiff.tex
	pdflatex msdiff
	bibtex msdiff
	pdflatex msdiff
	pdflatex msdiff

main:
	pdflatex ms
	bibtex ms
	pdflatex ms
	pdflatex ms
    
update: gitupdate main diff
	cp ms.pdf ~/public_html/data/ms.pdf
	cp msdiff.pdf ~/public_html/data/msdiff.pdf

gitupdate:
	git checkout master
	git pull origin master