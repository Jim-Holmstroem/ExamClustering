
cut:
	ipython -i main.py

convert:
	mkdir output
	gs -dNOPAUSE -dBATCH -dSAFER -sDEVICE=png256 -dDownScaleFactor=1 -r600 -sOutputFile='output/page_%03d.png' extentor2.pdf
