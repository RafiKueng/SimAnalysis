all:
	latexdiff ms-before.tex ms.tex > msdiff.tex
	pdflatex msdiff
	bibtex msdiff
	pdflatex msdiff
	pdflatex msdiff

clean:
	rm -f *.aux *.log *.bbl *.blg *~
