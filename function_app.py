import logging,datetime,sys, os
import azure.functions as func
from utils.utils import save_input_as_md
from crews.content_generation.main import main as execute_content_generation_crew

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = func.FunctionApp()

@app.function_name(name="post_automation_trigger")
@app.schedule(schedule="*/10 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False)
def post_automation_trigger(myTimer: func.TimerRequest) -> None:
    
    inputs = {
        "topic": "Adquicision de clientes para una fintech",
        "year": datetime.datetime.now().year,
        "month": datetime.datetime.now().month
    }

    result = execute_content_generation_crew(inputs)

    save_input_as_md(result.raw, f"content_{datetime.datetime.now().year}_{datetime.datetime.now().month}.md")

    logging.info('Python timer trigger function executed.')

post_automation_trigger()