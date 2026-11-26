# LNL PAC proposal in the official LNL template (Indico 50487): abstract.tex (1 page) + body.tex (<= 4 pages).
# make      -> abstract.pdf, body.pdf (separately, for the Indico upload), main.pdf (both in one, as Overleaf shows it)
# make zip  -> ../out/lnl_x17_pac_proposal.zip (for Overleaf)
# Needs revtex4 (Overleaf has it; locally: texlive-publishers, or revtex4/ + revtex/ in ~/texmf/tex/latex).
FIGS = figures/fig1a_ntof_photo.jpg figures/fig1b_ntof_fans.png figures/fig_event.pdf figures/fig_acceptance.pdf figures/fig_predictions.pdf figures/fig_road.pdf
TEX = pdflatex -interaction=nonstopmode -halt-on-error
all: proposal.pdf main.pdf
%.pdf: %.tex preamble.tex macros.tex abstract_content.tex body_content.tex $(FIGS)
	$(TEX) $< >/dev/null && $(TEX) $< >/dev/null
proposal.pdf: abstract.pdf body.pdf
	pdfunite abstract.pdf body.pdf proposal.pdf
	@echo "body: $$(pdfinfo body.pdf | awk '/Pages/{print $$2}') pages (limit 4)"
zip: proposal.pdf main.pdf
	mkdir -p ../out && rm -f ../out/lnl_x17_pac_proposal.zip && zip -q ../out/lnl_x17_pac_proposal.zip main.tex abstract.tex body.tex preamble.tex abstract_content.tex body_content.tex macros.tex $(FIGS) README_overleaf.txt
clean:
	rm -f *.aux *.log *.out *.toc
.PHONY: all zip clean
