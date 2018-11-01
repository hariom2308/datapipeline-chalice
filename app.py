"""Main Chalice File"""

import logging
from sqlalchemy import create_engine
from chalice import Chalice
from chalicelib import execute

app = Chalice(app_name='datapipeline-chalice')
logger = app.log
logger.setLevel(logging.DEBUG)


@app.route('/report', methods=['POST']) # {report: '1', bucket: 'name' , key: 'name'}
def main():
    try:
        logger.info("Starting main()")
        report_num = execute.select_report(app.current_request.json_body['report'])
        bucket = app.current_request.json_body['bucket']
        key = app.current_request.json_body['key']
        execute.executor(report_num, bucket, key)
        logger.info("Finished execution.")
        return {"Success": "Finished execution"}
    except Exception as e:
        logger.error(e.args[0])
