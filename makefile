PAGES_DIRECTORY = pages

cut:
	ipython -i main.py

convert:
	mkdir ${PAGES_DIRECTORY}
	gs -dNOPAUSE -dBATCH -dSAFER -sDEVICE=png256 -dDownScaleFactor=1 -r600 -sOutputFile='${PAGES_DIRECTORY}/page_%03d.png' extentor2.pdf
