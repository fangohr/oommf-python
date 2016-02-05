classes.pdf: classes.org *.eps
	emacs --script org-files-to-pdf.el

force:
	rm classes.pdf
	make classes.pdf

clean:
	rm -rf *.tex *.pdf *.tex~
	rm -rf _minted-*
	rm -rf .hypothesis

manual:
	pdflatex -shell-escape classes.tex

skim-start:
	make skim
	open -a skim classes-skim.pdf
	watch -n 1 make skim
