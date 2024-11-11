import logging,datetime,sys, os
import azure.functions as func
from utils.utils import save_input_as_md
from flows.flow_generation_content.main import execute_content_generation_flow

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = func.FunctionApp()

@app.function_name(name="post_automation_trigger")
@app.schedule(schedule="*/10 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False)
def post_automation_trigger(myTimer: func.TimerRequest ) -> None:

    result = execute_content_generation_flow()

    save_input_as_md(result, f"content_{datetime.datetime.now().year}_{datetime.datetime.now().month}.md")

    logging.info('Python timer trigger function executed.')