from gerador_capa.app import gerar_prompt


def test_gerar_prompt():
    titulo = "Python para iniciantes"
    tema = "minimalista"
    esperado = (
        "Uma capa de livro digital com o título 'Python para iniciantes',"
        " estilo minimalista, em design moderno e visual atrativo,"
        " com fundo limpo e elementos criativos."
    )

    # Act
    prompt = gerar_prompt(titulo, tema)

    # Assert
    assert prompt == esperado
