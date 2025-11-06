import unittest
from core.lexer import Lexer, Token
from utilidades import tokens
from utilidades.tokens import TOKEN_TYPES, KEYWORDS, SYMBOLS

class TestLexer(unittest.TestCase):

    def test_basic_script(self):
        script = '''
        # Script de prueba
        set name = "HOLAAAA"
        copy "prueba.txt" to "descargas/prueba.txt"
        '''
        lexer = Lexer(script)
        tokens = lexer.tokenize()
        print("\n-------TOKENS DE UNITTEST -------")
        for t in tokens:
            print(t)  
        print("-------FIN DE TOKENS -------\n")


        # Comprobamos que los tokens fundamentales existan en orden
        expected_types = [
            KEYWORDS["set"], TOKEN_TYPES["VAR"], SYMBOLS["="], TOKEN_TYPES["STRING"],
            KEYWORDS["copy"], TOKEN_TYPES["STRING"], KEYWORDS["to"], TOKEN_TYPES["STRING"],
            TOKEN_TYPES["END"]
        ]
        self.assertEqual([token.type for token in tokens], expected_types)

    def test_if_else_block(self):
        script = '''
        if exists "descargas/prueba.txt" {
            log "Archivo copiado :)"
        } else {
            log "No se pudo copiar :("
        }
        '''

        lexer = Lexer(script)
        tokens = lexer.tokenize()

        # validar END y no falle
        self.assertEqual(tokens[-1].type, TOKEN_TYPES["END"])
        self.assertTrue(any(token.type == KEYWORDS["if"] for token in tokens))

if __name__ == '__main__':
    unittest.main()
