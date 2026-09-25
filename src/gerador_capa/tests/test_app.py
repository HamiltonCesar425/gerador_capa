import base64
from io import BytesIO
from unittest.mock import Mock

from PIL import Image

from gerador_capa.app import gerar_imagem, gerar_prompt, salvar_imagem


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


def test_gerar_imagem():
    # Arrange
    prompt = "Uma capa minimalista"
    cliente_imagem = Mock()

    resposta_mock = Mock()
    resposta_mock.data = [Mock(b64_json="imagem_em_base64")]
    cliente_imagem.generate.return_value = resposta_mock

    # Act
    resultado = gerar_imagem(prompt, cliente_imagem)

    # Assert
    assert resultado == "imagem_em_base64"

    cliente_imagem.generate.assert_called_once_with(
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )


def test_salvar_imagem_cria_arquivo_png(tmp_path):
    # Arrange
    imagem = Image.new("RGB", (1, 1))
    buffer = BytesIO()
    imagem.save(buffer, format="PNG")
    imagem_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    nome_arquivo = tmp_path / "capa_teste"

    # Act
    salvar_imagem(imagem_base64, nome_arquivo)

    # Assert
    arquivo_esperado = tmp_path / "capa_teste.png"
    assert arquivo_esperado.exists()

    with Image.open(arquivo_esperado) as imagem_salva:
        assert imagem_salva.format == "PNG"
