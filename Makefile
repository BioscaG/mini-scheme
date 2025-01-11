ANTLR=antlr4
GRAMMAR=scheme.g4
OUTPUT_DIR=.
LANGUAGE=Python3

all: generate

generate:
	$(ANTLR) -Dlanguage=$(LANGUAGE) -no-listener -visitor $(GRAMMAR)

clean:
	rm -f $(OUTPUT_DIR)/*Lexer.py
	rm -f $(OUTPUT_DIR)/*Parser.py
	rm -f $(OUTPUT_DIR)/*Visitor.py
	rm -f $(OUTPUT_DIR)/*Listener.py
	rm -f $(OUTPUT_DIR)/*.tokens
	rm -f $(OUTPUT_DIR)/*.interp

# Ayuda
help:
	@echo "Opciones disponibles:"
	@echo "  make generate   - Generar lexer y parser con ANTLR."
	@echo "  make clean      - Eliminar archivos generados por ANTLR."
	@echo "  make help       - Mostrar esta ayuda."
