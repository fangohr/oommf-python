classes.pdf: classes.org *.eps
	emacs --script org-files-to-pdf.el

force:
	rm classes.pdf
	make classes.pdf

clean:
	rm -rf *.tex *.pdf *.tex~

manual:
	pdflatex classes.tex
