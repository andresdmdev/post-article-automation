import logging, datetime, sys, os
from azure.functions import FunctionApp, TimerRequest
from utils.utils import save_input_as_md
from flows.flow_generation_content.main import execute_content_generation_flow
from flows.flow_social_network_content.main import execute_social_network_content_flow

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FunctionApp()

@app.function_name(name="post_automation_trigger")
@app.timer_trigger(
    schedule="0 0 0 1 * *",  # Formato cron de 6 campos (segundo incluido)
    arg_name="myTimer",
    run_on_startup=True
)
def main(myTimer: TimerRequest) -> None:
    result = execute_content_generation_flow()
    execute_social_network_content_flow()
    save_input_as_md(result, f"content_{datetime.datetime.now().year}_{datetime.datetime.now().month}.md")
    logging.info('Trigger ejecutado correctamente a las %s', datetime.datetime.now().isoformat())