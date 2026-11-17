set -e
cd /home/claude/odsv/pptx/_build; python3 deck.py
cd ..; S=/mnt/skills/public/pptx/scripts
python3 $S/office/validate.py ODSV-Vorlage.pptx 2>&1 | tail -8
cd _preview; rm -f *.png *.pdf; python3 $S/office/soffice.py --headless --convert-to pdf ../ODSV-Vorlage.pptx >/dev/null 2>&1
pdftoppm -png -r 80 ODSV-Vorlage.pdf slide-raw
