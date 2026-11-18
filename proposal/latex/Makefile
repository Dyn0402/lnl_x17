# make      -> main.pdf ;  make zip -> ../out/lnl_x17_pac_proposal.zip (for Overleaf upload)
main.pdf: main.tex figures/limit_vs_days.pdf
	pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null && pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
zip: main.pdf
	mkdir -p ../out && rm -f ../out/lnl_x17_pac_proposal.zip && zip -q ../out/lnl_x17_pac_proposal.zip main.tex figures/*.pdf README_overleaf.txt
clean:
	rm -f *.aux *.log *.out *.toc
