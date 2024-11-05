import os
from dotenv import load_dotenv, find_dotenv

def load_env():
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key

def get_serper_api_key():
    load_env()
    openai_api_key = os.getenv("SERPER_API_KEY")
    return openai_api_key

def pretty_print_result(result):
  parsed_result = []
  for line in result.split('\n'):
      if len(line) > 80:
          words = line.split(' ')
          new_line = ''
          for word in words:
              if len(new_line) + len(word) + 1 > 80:
                  parsed_result.append(new_line)
                  new_line = word
              else:
                  if new_line == '':
                      new_line = word
                  else:
                      new_line += ' ' + word
          parsed_result.append(new_line)
      else:
          parsed_result.append(line)
  return "\n".join(parsed_result)

def save_input_as_md(input_text, filename):
    """
    Guarda el texto de entrada como un archivo .md en el directorio actual.

    :param input_text: El texto que se guardará en el archivo.
    :param filename: El nombre del archivo (sin extensión).
    """
    # Asegúrate de que el nombre del archivo tenga la extensión .md
    if not filename.endswith('.md'):
        filename += '.md'
    
    # Obtén la ruta completa del archivo en el directorio actual
    file_path = os.path.join(os.getcwd(), filename)
    
    # Escribe el texto de entrada en el archivo
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(input_text)
    
    print(f"Archivo guardado como {file_path}")

