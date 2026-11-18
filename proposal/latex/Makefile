# LNL PAC proposal in the official LNL template (Indico 50487): abstract.tex (1 page) + body.tex (<= 4 pages).
# make      -> abstract.pdf, body.pdf, proposal.pdf (both, for the Indico upload)
# make zip  -> ../out/lnl_x17_pac_proposal.zip (for Overleaf)
# Needs revtex4 (Overleaf has it; locally: texlive-publishers, or revtex4/ + revtex/ in ~/texmf/tex/latex).
TEX = pdflatex -interaction=nonstopmode -halt-on-error
all: proposal.pdf
%.pdf: %.tex macros.tex figures/limit_vs_days.pdf
	$(TEX) $< >/dev/null && $(TEX) $< >/dev/null
proposal.pdf: abstract.pdf body.pdf
	pdfunite abstract.pdf body.pdf proposal.pdf
	@echo "body: $$(pdfinfo body.pdf | awk '/Pages/{print $$2}') pages (limit 4)"
zip: proposal.pdf
	mkdir -p ../out && rm -f ../out/lnl_x17_pac_proposal.zip && zip -q ../out/lnl_x17_pac_proposal.zip abstract.tex body.tex macros.tex figures/*.pdf README_overleaf.txt
clean:
	rm -f *.aux *.log *.out *.toc
.PHONY: all zip clean
