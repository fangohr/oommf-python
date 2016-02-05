#!/usr/bin/env emacs --script
;; Emacs script for exporting all org files in current directory to pdf
;; using LaTeX and beamer.
;;
;; This requires Emacs 24.2 or Org-mode 8.0 and was tested on OSX
;; using Emacs 23.4.93.1 and Org 8.2.6

;; Author: Sam Sinayoko
;; Email: s.sinayoko@soton.ac.uk
;; Date: 05/10/2014

(require 'ox-beamer)
(require 'ox-latex)

;; Define an interactive function for easy testing
(defun org-beamer-export-to-pdf-directory (dirname)
  "Export all org files in directory `dirname' to pdf"
  (interactive "DExport org files to pdf in directory:")
  (save-excursion
    (let ((org-files-lst ))
      (dolist (org-file (directory-files dirname nil "\.org$"))
	(message "*** Exporting file %s ***" org-file)
	(find-file org-file)
	(org-beamer-export-to-pdf)
	(kill-buffer)))))


;;       (dolist (org-file (directory-files dirname nil "\.org$"))

;; Don't evaluate the blocks
;; (all the results must evaluated beforehand and the results stored in the org file)
(setq org-export-babel-evaluate nil)

;; Make the code blocks look nicer
(add-to-list 'org-latex-packages-alist '("" "minted"))
(add-to-list 'org-latex-packages-alist '("" "fancyvrb"))
(setq org-latex-listings 'minted)
(setq org-latex-pdf-process
      '("pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"
	"pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"
	"pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"))
(setq org-latex-minted-options
      '(("bgcolor" "white") ("frame" "lines")))

;; Make the results block look nicer with package fancyvrb
;; The package fancyvrb must be included in the org-file header
(defun org-latex-filter-fancyvrb (text backend info)
      "Convert begin/end{verbatim} to begin/end{Verbatim}.
    Allows use of the fancyvrb latex package."
      (when (or (org-export-derived-backend-p backend 'beamer)
                (org-export-derived-backend-p backend 'latex))
        (replace-regexp-in-string
         "\\\\\\(begin\\|end\\){verbatim}"
         "\\\\\\1{Verbatim}"
         text)))

(add-to-list 'org-export-filter-final-output-functions
	     'org-latex-filter-fancyvrb)


;; Add the environment "onlyenv" to display something only on certain slides
(add-to-list 'org-beamer-environments-extra
             '("onlyenv" "O" "\\begin{onlyenv}%a" "\\end{onlyenv}"))

;; Use utf8x for LaTeX export to access more unicode characters
(setq org-latex-inputenc-alist '(("utf8" . "utf8x")))

;; Export all org files
(org-beamer-export-to-pdf-directory ".")
