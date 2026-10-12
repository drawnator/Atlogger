import logging
#TODO try to import and if unable stop importing this file
import wandb
from logging import LogRecord

class WandbHandler(logging.Handler):
  """Handler that enables logging to coreweave's weights and biases
  Args:
  *args: passed along to parent
  key: use to manually pass API key to wandb login, not recomended.
    If needed it is best to login from outside of the handler initialization
  project: project name where it will be logged to
  config: aditional configuration information to be logged at the start of the run
    Recommend importing yaml or json configs as dicts and passing as this parameter
  run: use this run instead of creating a new one. serves to continue after a stop
  **kwargs: passed along to parent
  """
  run:wandb.Run=None
  def __init__(self,
  *args,
  key:str="",
  project:str="unamed_project",
  config:dict={},
  run:wandb.Run=None,
  **kwargs):
    logging.Handler.__init__(self,*args,**kwargs)
    if key != "":
      wandb.login(key)
    else:
      wandb.login()
    if run is not None:
      self.run = run
    else:
      self.run = wandb.init(project=project,config=config)

  #TODO convert record.msg in json serializable before logging
  #or try yo log and convert with _repr_() if unable 
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