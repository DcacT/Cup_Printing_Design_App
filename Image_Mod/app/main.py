from .models.models_main import Model
from .views.views_main import View
from .controllers.controllers_main import Controller
import logging
import argparse
from .sql.sql_helper import sql, reset
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(filename)s] %(message)s"
)
logging.getLogger("PIL").setLevel(logging.WARNING)



def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', type=bool, default=False)
    parser.add_argument('--test', type=bool, default=False)
    args = parser.parse_args()
    
    if (args.reset):
        logging.critical('Resetting Everything')
        reset()
   
    
    logging.info("App Start")
    model = Model()
    view = View()
    controller = Controller(model, view)
    
    if (args.test):
        model.template_manager.test() 
    
    controller.start()

if __name__ == "__main__":
    main()