import base64
from io import BytesIO
from unittest.mock import Mock

import pytest
from PIL import Image, UnidentifiedImageError

from gerador_capa import app
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


def test_gerar_imagem_com_resposta_sem_dados():
    cliente_imagem = Mock()
    cliente_imagem.generate.return_value = Mock(data=[])

    with pytest.raises(ValueError, match="A API não retornou dados de imagem."):
        gerar_imagem("prompt de teste", cliente_imagem)


def test_salvar_imagem_com_base64_invalido():
    with pytest.raises(ValueError):
        salvar_imagem("isto-nao-e-base64!!!", "imagem_teste")


def test_salvar_imagem_com_base64_que_nao_contem_imagem():
    conteudo = b"isto e apenas texto"
    imagem_base64 = base64.b64encode(conteudo).decode("utf-8")

    with pytest.raises(UnidentifiedImageError):
        salvar_imagem(imagem_base64, "imagem_teste")


def test_salvar_imagem_com_erro_ao_gravar(monkeypatch):
    # Arrange
    conteudo = base64.b64encode(b"conteudo de teste").decode("utf-8")

    imagem_mock = Mock()
    imagem_mock.save.side_effect = OSError("Falha ao gravar arquivo")

    monkeypatch.setattr(app.Image, "open", Mock(return_value=imagem_mock))

    # Act & Assert
    with pytest.raises(OSError, match="Falha ao gravar arquivo"):
        salvar_imagem(conteudo, "imagem_teste")


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


def test_main_orquestra_fluxo(monkeypatch):
    # Arrange
    cliente_mock = Mock()
    monkeypatch.setattr(app, "OpenAI", Mock(return_value=cliente_mock))

    entradas = iter(["Python para iniciantes", "minimalista"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    gerar_imagem_mock = Mock(return_value="imagem_em_base64")
    salvar_imagem_mock = Mock()

    monkeypatch.setattr(app, "gerar_imagem", gerar_imagem_mock)
    monkeypatch.setattr(app, "salvar_imagem", salvar_imagem_mock)

    # Act
    app.main()

    # Assert
    prompt_esperado = (
        "Uma capa de livro digital com o título 'Python para iniciantes',"
        " estilo minimalista, em design moderno e visual atrativo,"
        " com fundo limpo e elementos criativos."
    )

    gerar_imagem_mock.assert_called_once_with(
        prompt_esperado,
        cliente_mock.images,
    )

    salvar_imagem_mock.assert_called_once_with(
        "imagem_em_base64",
        "Python_para_iniciantes",
    )


def test_main_trata_erro_ao_gerar_imagem(monkeypatch, capsys):
    # Arrange
    cliente_mock = Mock()
    monkeypatch.setattr(app, "OpenAI", Mock(return_value=cliente_mock))

    entradas = iter(["Python para iniciantes", "minimalista"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    gerar_imagem_mock = Mock(
        side_effect=ValueError("A API não retornou dados de imagem.")
    )
    salvar_imagem_mock = Mock()

    monkeypatch.setattr(app, "gerar_imagem", gerar_imagem_mock)
    monkeypatch.setattr(app, "salvar_imagem", salvar_imagem_mock)

    # Act
    app.main()

    # Assert
    saida = capsys.readouterr()

    assert "A API não retornou dados de imagem." in saida.out
    salvar_imagem_mock.assert_not_called()


def test_main_trata_erro_ao_salvar_imagem(monkeypatch, capsys):
    # Arrange
    cliente_mock = Mock()
    monkeypatch.setattr(app, "OpenAI", Mock(return_value=cliente_mock))

    entradas = iter(["Python para iniciantes", "minimalista"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    monkeypatch.setattr(
        app,
        "gerar_imagem",
        Mock(return_value="imagem_em_base64"),
    )

    salvar_imagem_mock = Mock(side_effect=OSError("Falha ao gravar arquivo"))
    monkeypatch.setattr(app, "salvar_imagem", salvar_imagem_mock)

    # Act
    app.main()

    # Assert
    saida = capsys.readouterr()

    assert "Falha ao gravar arquivo" in saida.out


def test_main_trata_base64_invalido_ao_salvar(monkeypatch, capsys):
    # Arrange
    cliente_mock = Mock()
    monkeypatch.setattr(app, "OpenAI", Mock(return_value=cliente_mock))

    entradas = iter(["Python para iniciantes", "minimalista"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    monkeypatch.setattr(
        app,
        "gerar_imagem",
        Mock(return_value="imagem_em_base64"),
    )

    salvar_imagem_mock = Mock(side_effect=ValueError("Conteúdo Base64 inválido"))
    monkeypatch.setattr(app, "salvar_imagem", salvar_imagem_mock)

    # Act
    app.main()

    # Assert
    saida = capsys.readouterr()

    assert "Conteúdo Base64 inválido" in saida.out
