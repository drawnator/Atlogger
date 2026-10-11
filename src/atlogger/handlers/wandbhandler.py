import logging
import wandb
from logging import LogRecord

class WandbHandler(logging.Handler):
  run:wandb.Run=None
  def __init__(self,
  *args,
  project:str="unamed_project",
  config:dict={},
  run:wandb.Run=None,
  **kwargs):
    logging.Handler.__init__(self,**kwargs)
    wandb.login()
    if run is not None:
      self.run = run
    else:
      self.run = wandb.init(project=project,config=config)
    
  def emit(self,record:LogRecord):
    variable_name = record.__dict__["_ATLOGGER_VARIABLENAME"]
    if type(record.msg) == tuple and len(variable_name) == len(record.msg):
      output = dict(zip(variable_name,record.msg))
      self.run.log(output)
    else:
      self.run.log({variable_name[0]:record.msg})

  def close(self):
    self.run.finish()
    super().close()