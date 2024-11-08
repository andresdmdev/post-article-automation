import os, json
from dotenv import load_dotenv, find_dotenv

def load_env():
    _ = load_dotenv(find_dotenv())

def load_openai_api_config():
    load_env()
    os.getenv("OPENAI_API_KEY")
    os.getenv("OPENAI_MODEL_NAME")

def load_serper_api_config():
    load_env()
    os.getenv("SERPER_API_KEY")

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
    if not filename.endswith('.md'):
        filename += '.md'
    
    file_path = os.path.join(os.getcwd(), filename)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(input_text)
    
    print(f"Save file {file_path}")

def get_topic_sets() -> list[str]:
    load_env()
    topics = os.getenv("DEFAULT_TOPICS")
    return json.loads(topics)