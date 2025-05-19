import sqlite3
import logging
import os
import shutil
logger = logging.getLogger(__name__)
self_path = os.path.dirname(os.path.realpath(__file__))

db_path= os.path.join(self_path,'data.db' )


def sql(prompt_msg):
    prompt_msg = prompt_msg.rstrip()
    logger.info(f'Executing SQL: {prompt_msg}')
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(prompt_msg)
            
            # if prompt_msg.strip().lower().startswith('select'):
            results = cursor.fetchall()
            return results
            
    except sqlite3.Error as e:
        logger.error(f"SQLite error: {e}")
        return e
        # raise

def reset():
    
    os.remove(db_path)
    with open(db_path, 'w') as db:
        pass

    #create config table  
    msg = '''
    CREATE TABLE TEMPLATES (
    folder_name VARCHAR(255) PRIMARY KEY,
    PX_Min FLOAT,
    PX_Max FLOAT,
    Horizontal_Limit FLOAT,
    Vertical_Limit FLOAT,
    Line_1_vx FLOAT,
    Line_1_vy FLOAT,
    Line_1_x0 FLOAT,
    Line_1_y0 FLOAT,
    Line_2_vx FLOAT,
    Line_2_vy FLOAT,
    Line_2_x0 FLOAT,
    Line_2_y0 FLOAT,
    Arc_1_x FLOAT,
    Arc_1_y FLOAT,
    Arc_1_r FLOAT,
    Arc_2_x FLOAT,
    Arc_2_y FLOAT,
    Arc_2_r FLOAT
    );
    '''
    sql(msg)