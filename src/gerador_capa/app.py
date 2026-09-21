import base64

from io import BytesIO
from PIL import Image


def gerar_prompt(titulo, tema):
    return f"Uma capa de livro digital com o título '{titulo}', estilo {tema}, em design moderno e visual atrativo, com fundo limpo e elementos criativos."


def gerar_imagem(prompt):
    response = openai.Image.create(
        prompt=prompt, n=1, size="1024x1024", response_format="b64_json"
    )
    imagem_base64 = response["data"][0]["b64_json"]
    return imagem_base64


def salvar_imagem(imagem_base64, nome_arquivo):
    imagem_bytes = base64.b64decode(imagem_base64)
    imagem = Image.open(BytesIO(imagem_bytes))
    imagem.save(f"{nome_arquivo}.png")
    print(f"Imagem salva como {nome_arquivo}.png")


def main():
    print("Gerador de Capa com IA (OpenAI DALL·E)")
    titulo = input("Digite o título do produto: ")
    tema = input(
        "Digite o tema ou estilo visual (ex: futurista, minimalista, retrô, etc.): "
    )

    prompt = gerar_prompt(titulo, tema)
    print(f"Prompt gerado: {prompt}")

    imagem_base64 = gerar_imagem(prompt)
    salvar_imagem(imagem_base64, titulo.replace(" ", "_"))


if __name__ == "__main__":
    main()
